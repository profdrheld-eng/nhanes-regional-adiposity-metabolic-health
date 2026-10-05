#!/usr/bin/env python3
"""Prespecified temporal ML benchmark. No test-cycle tuning."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from survey_bootstrap import rescaled_psu_factors
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    log_loss,
    roc_auc_score,
)
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, SplineTransformer, StandardScaler
from xgboost import XGBClassifier


PROJECT = Path(__file__).resolve().parents[2]
DERIVED = PROJECT / "02_data" / "derived"
RESULTS = PROJECT / "04_outputs" / "results"
MODELS = PROJECT / "03_analysis" / "models"
RESULTS.mkdir(parents=True, exist_ok=True)
MODELS.mkdir(parents=True, exist_ok=True)
CONFIG = json.loads((PROJECT / "03_analysis" / "config" / "frozen-analysis.json").read_text())
SEED = int(CONFIG["seed"])

data = pd.read_csv(DERIVED / "harmonized_analysis_data.csv", low_memory=False)
data["primary_domain"] = data["primary_domain"].astype(str).str.lower().eq("true")
data = data.loc[data["primary_domain"]].copy()
data["outcome"] = data["metabolic_dysfunction"].astype(str).str.lower().eq("true").astype(int)

categorical = ["sex", "race_ethnicity", "cycle", "education", "smoking"]
panels = {
    "A_base": ["RIDAGEYR", "sex", "race_ethnicity", "cycle", "education", "INDFMPIR", "smoking"],
    "B_bmi": ["RIDAGEYR", "sex", "race_ethnicity", "cycle", "education", "INDFMPIR", "smoking", "BMXBMI"],
    "C_bmi_waist": [
        "RIDAGEYR", "sex", "race_ethnicity", "cycle", "education", "INDFMPIR",
        "smoking", "BMXBMI", "BMXWAIST",
    ],
    "D_dxa": [
        "RIDAGEYR", "sex", "race_ethnicity", "cycle", "education", "INDFMPIR",
        "smoking", "BMXBMI", "BMXWAIST", "total_fmi", "log_leg_trunk_ratio",
        "ag_ratio", "vat_kg",
    ],
}

development = data[data["cycle"].isin(CONFIG["ml_development_cycles"])].copy()
test = data[data["cycle"].eq(CONFIG["ml_test_cycle"])].copy()
if development.empty or test.empty:
    raise RuntimeError("Development or protected test population is empty.")


def normalized_weight(frame: pd.DataFrame) -> np.ndarray:
    weight = frame["pooled_fasting_weight"].to_numpy(dtype=float)
    return weight / np.mean(weight)


def checked_probability(model: Pipeline, frame: pd.DataFrame) -> np.ndarray:
    transformed = model.named_steps["features"].transform(frame)
    if not np.isfinite(transformed).all():
        raise RuntimeError("The fitted preprocessing pipeline produced non-finite values.")
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        probability = model.named_steps["model"].predict_proba(transformed)[:, 1]
    if not np.isfinite(probability).all() or np.any((probability < 0) | (probability > 1)):
        raise RuntimeError("The fitted model produced invalid probabilities.")
    return probability


def preprocessor(features: list[str], spline: bool = False) -> ColumnTransformer:
    cats = [x for x in features if x in categorical]
    nums = [x for x in features if x not in categorical]
    numeric_steps = [("impute", SimpleImputer(strategy="median"))]
    if spline:
        numeric_steps += [
            ("scale", StandardScaler()),
            (
                "spline",
                SplineTransformer(
                    n_knots=5,
                    degree=3,
                    include_bias=False,
                    extrapolation="constant",
                ),
            ),
        ]
    else:
        numeric_steps += [("scale", StandardScaler())]
    return ColumnTransformer(
        [
            ("numeric", Pipeline(numeric_steps), nums),
            (
                "categorical",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                    ]
                ),
                cats,
            ),
        ],
        verbose_feature_names_out=False,
    )


def candidates(model_name: str, features: list[str]):
    if model_name == "penalized_logistic":
        return [
            (
                {"C": c},
                Pipeline(
                    [
                        ("features", preprocessor(features)),
                        (
                            "model",
                            LogisticRegression(
                                C=c, penalty="l2", solver="liblinear", max_iter=2000,
                                random_state=SEED,
                            ),
                        ),
                    ]
                ),
            )
            for c in (0.1, 1.0, 10.0)
        ]
    if model_name == "spline_logistic":
        return [
            (
                {"C": c, "n_knots": 5},
                Pipeline(
                    [
                        ("features", preprocessor(features, spline=True)),
                        (
                            "model",
                            LogisticRegression(
                                C=c, penalty="l2", solver="liblinear", max_iter=3000,
                                random_state=SEED,
                            ),
                        ),
                    ]
                ),
            )
            for c in (0.1, 1.0, 10.0)
        ]
    if model_name == "xgboost":
        settings = [
            (2, 0.03, 250),
            (3, 0.03, 250),
            (3, 0.05, 180),
        ]
        return [
            (
                {"max_depth": depth, "learning_rate": lr, "n_estimators": n},
                Pipeline(
                    [
                        ("features", preprocessor(features)),
                        (
                            "model",
                            XGBClassifier(
                                max_depth=depth,
                                learning_rate=lr,
                                n_estimators=n,
                                min_child_weight=5,
                                subsample=0.8,
                                colsample_bytree=0.8,
                                reg_lambda=2.0,
                                objective="binary:logistic",
                                eval_metric="logloss",
                                random_state=SEED,
                                n_jobs=1,
                            ),
                        ),
                    ]
                ),
            )
            for depth, lr, n in settings
        ]
    raise ValueError(model_name)


def tune(model_name: str, features: list[str]):
    groups = development["cycle"].to_numpy()
    splitter = GroupKFold(n_splits=len(np.unique(groups)))
    rows = []
    best = None
    for params, prototype in candidates(model_name, features):
        losses = []
        for train_idx, valid_idx in splitter.split(development, development["outcome"], groups):
            train = development.iloc[train_idx]
            valid = development.iloc[valid_idx]
            model = clone(prototype)
            model.fit(
                train[features],
                train["outcome"],
                model__sample_weight=normalized_weight(train),
            )
            transformed = model.named_steps["features"].transform(valid[features])
            if not np.isfinite(transformed).all():
                raise RuntimeError(
                    f"Non-finite transformed values for {model_name}, {params}, "
                    f"validation cycle {valid['cycle'].iloc[0]}."
                )
            if np.max(np.abs(transformed)) > 1e6:
                raise RuntimeError(
                    f"Extreme transformed value {np.max(np.abs(transformed))} for "
                    f"{model_name}, {params}, validation cycle {valid['cycle'].iloc[0]}."
                )
            fitted_model = model.named_steps["model"]
            if hasattr(fitted_model, "coef_"):
                if not np.isfinite(fitted_model.coef_).all():
                    raise RuntimeError(
                        f"Non-finite coefficient for {model_name}, {params}, "
                        f"validation cycle {valid['cycle'].iloc[0]}."
                    )
                if np.max(np.abs(fitted_model.coef_)) > 1e6:
                    raise RuntimeError(
                        f"Extreme coefficient {np.max(np.abs(fitted_model.coef_))} for "
                        f"{model_name}, {params}, validation cycle {valid['cycle'].iloc[0]}."
                    )
            probability = checked_probability(model, valid[features])
            losses.append(
                log_loss(
                    valid["outcome"], probability,
                    sample_weight=valid["pooled_fasting_weight"], labels=[0, 1],
                )
            )
        mean_loss = float(np.mean(losses))
        rows.append({"parameters": json.dumps(params, sort_keys=True), "cv_log_loss": mean_loss, "fold_log_losses": json.dumps(losses)})
        key = (round(mean_loss, 6), json.dumps(params, sort_keys=True))
        if best is None or key < best[0]:
            best = (key, params, prototype)
    return best[1], best[2], rows


def calibration(y, p, w):
    clipped = np.clip(p, 1e-6, 1 - 1e-6)
    lp = np.log(clipped / (1 - clipped))
    normalized = w / np.mean(w)
    fit = sm.GLM(
        y,
        sm.add_constant(lp),
        family=sm.families.Binomial(),
        freq_weights=normalized,
    ).fit()
    return float(fit.params[0]), float(fit.params[1])


metrics = []
tuning_rows = []
predictions = test[
    [
        "SEQN",
        "cycle",
        "sex",
        "outcome",
        "pooled_fasting_weight",
        "SDMVSTRA",
        "SDMVPSU",
    ]
].copy()

for panel_name, features in panels.items():
    for model_name in CONFIG["ml_models"]:
        selected_params, prototype, rows = tune(model_name, features)
        for row in rows:
            tuning_rows.append({"panel": panel_name, "model": model_name, **row})
        model = clone(prototype)
        model.fit(
            development[features],
            development["outcome"],
            model__sample_weight=normalized_weight(development),
        )
        probability = checked_probability(model, test[features])
        y = test["outcome"].to_numpy()
        w = test["pooled_fasting_weight"].to_numpy()
        intercept, slope = calibration(y, probability, w)
        metrics.append(
            {
                "panel": panel_name,
                "model": model_name,
                "selected_parameters": json.dumps(selected_params, sort_keys=True),
                "development_n": len(development),
                "test_n": len(test),
                "weighted_auc": roc_auc_score(y, probability, sample_weight=w),
                "weighted_average_precision": average_precision_score(y, probability, sample_weight=w),
                "weighted_log_loss": log_loss(y, probability, sample_weight=w, labels=[0, 1]),
                "weighted_brier": brier_score_loss(y, probability, sample_weight=w),
                "calibration_intercept": intercept,
                "calibration_slope": slope,
            }
        )
        predictions[f"{panel_name}__{model_name}"] = probability
        import joblib

        joblib.dump(model, MODELS / f"{panel_name}__{model_name}.joblib")

        if panel_name == "D_dxa" and model_name == "xgboost":
            feature_names = model.named_steps["features"].get_feature_names_out()
            importance = model.named_steps["model"].feature_importances_
            pd.DataFrame(
                {"feature": feature_names, "gain_importance": importance}
            ).sort_values("gain_importance", ascending=False).to_csv(
                RESULTS / "xgboost_dxa_feature_importance.csv", index=False
            )

metric_frame = pd.DataFrame(metrics)
pd.DataFrame(tuning_rows).to_csv(RESULTS / "ml_development_tuning.csv", index=False)
predictions.to_csv(DERIVED / "protected_test_predictions.csv", index=False)

bootstrap_source = predictions.reset_index(drop=True)
probability_columns = [column for column in bootstrap_source if "__" in column]
strata_clusters = []
for _, stratum in bootstrap_source.groupby("SDMVSTRA", sort=True):
    cluster_rows = {
        psu: stratum.index[stratum["SDMVPSU"].eq(psu)].to_numpy()
        for psu in sorted(stratum["SDMVPSU"].unique())
    }
    strata_clusters.append(cluster_rows)

rng = np.random.default_rng(SEED)
bootstrap_rows = []
bootstrap_replicates = int(CONFIG["ml_test_uncertainty_bootstrap_replicates"])
for replicate in range(bootstrap_replicates):
    factors = rescaled_psu_factors(
        bootstrap_source.SDMVSTRA.to_numpy(), bootstrap_source.SDMVPSU.to_numpy(), rng)
    sampled = bootstrap_source.loc[factors > 0].copy()
    sampled["pooled_fasting_weight"] *= factors[factors > 0]
    if sampled["outcome"].nunique() < 2:
        continue
    for column in probability_columns:
        panel_name, model_name = column.split("__", maxsplit=1)
        ci_intercept, ci_slope = calibration(sampled["outcome"].to_numpy(), sampled[column].to_numpy(), sampled["pooled_fasting_weight"].to_numpy())
        bootstrap_rows.append(
            {
                "replicate": replicate,
                "calibration_intercept": ci_intercept,
                "calibration_slope": ci_slope,
                "panel": panel_name,
                "model": model_name,
                "weighted_auc": roc_auc_score(
                    sampled["outcome"],
                    sampled[column],
                    sample_weight=sampled["pooled_fasting_weight"],
                ),
            }
        )

bootstrap_frame = pd.DataFrame(bootstrap_rows)
bootstrap_frame.to_csv(RESULTS / "ml_bootstrap_auc_replicates.csv", index=False)
calibration_summary = bootstrap_frame.groupby(["panel", "model"])[["calibration_intercept", "calibration_slope"]].quantile([0.025,0.975])
calibration_summary.to_csv(RESULTS / "ml_calibration_intervals.csv")
bootstrap_summary = (
    bootstrap_frame.groupby(["panel", "model"])
    .weighted_auc.agg(
        bootstrap_valid_replicates="count",
        auc_ci_low=lambda x: np.quantile(x, 0.025),
        auc_ci_high=lambda x: np.quantile(x, 0.975),
    )
    .reset_index()
)
bootstrap_summary.to_csv(RESULTS / "ml_temporal_auc_bootstrap.csv", index=False)
metric_frame = metric_frame.merge(bootstrap_summary, on=["panel", "model"], how="left")
metric_frame.to_csv(RESULTS / "ml_temporal_metrics.csv", index=False)

incremental = []
for model_name in CONFIG["ml_models"]:
    c = metric_frame[(metric_frame.panel == "C_bmi_waist") & (metric_frame.model == model_name)].iloc[0]
    d = metric_frame[(metric_frame.panel == "D_dxa") & (metric_frame.model == model_name)].iloc[0]
    model_bootstrap = bootstrap_frame[bootstrap_frame.model.eq(model_name)].pivot(
        index="replicate", columns="panel", values="weighted_auc"
    )
    auc_difference = model_bootstrap["D_dxa"] - model_bootstrap["C_bmi_waist"]
    incremental.append(
        {
            "model": model_name,
            "delta_auc_dxa_minus_bmi_waist": d.weighted_auc - c.weighted_auc,
            "delta_auc_ci_low": np.quantile(auc_difference, 0.025),
            "delta_auc_ci_high": np.quantile(auc_difference, 0.975),
            "delta_brier_dxa_minus_bmi_waist": d.weighted_brier - c.weighted_brier,
            "delta_log_loss_dxa_minus_bmi_waist": d.weighted_log_loss - c.weighted_log_loss,
        }
    )
pd.DataFrame(incremental).to_csv(RESULTS / "ml_incremental_value.csv", index=False)

print(f"ML benchmark complete: development n={len(development)}, protected test n={len(test)}")
