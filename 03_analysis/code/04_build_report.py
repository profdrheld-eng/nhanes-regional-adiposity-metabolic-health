#!/usr/bin/env python3
"""Create publication-facing tables, figures, and concise Methods/Results drafts."""

import os
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
os.environ.setdefault(
    "MPLCONFIGDIR",
    str(PROJECT / "03_analysis" / "environment" / "matplotlib-cache"),
)
os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


RESULTS = PROJECT / "04_outputs" / "results"
TABLES = PROJECT / "04_outputs" / "tables"
FIGURES = PROJECT / "04_outputs" / "figures"
REPORT_FRAGMENTS = PROJECT / "04_outputs" / "report_fragments"
for directory in (TABLES, FIGURES, REPORT_FRAGMENTS):
    directory.mkdir(parents=True, exist_ok=True)

quality = pd.read_csv(RESULTS / "data_quality_checks.csv")
q = dict(zip(quality.metric, quality.value))
contrasts = pd.read_csv(RESULTS / "primary_sex_contrasts.csv")
coefficients = pd.read_csv(RESULTS / "primary_model_coefficients.csv")
sensitivities = pd.read_csv(RESULTS / "sensitivity_model_coefficients.csv")
components = pd.read_csv(RESULTS / "secondary_component_sex_contrasts.csv")
table1 = pd.read_csv(RESULTS / "table1_publication.csv")
curve = pd.read_csv(RESULTS / "adjusted_prediction_curve.csv")
ml = pd.read_csv(RESULTS / "ml_temporal_metrics.csv")
incremental = pd.read_csv(RESULTS / "ml_incremental_value.csv")

contrasts.to_csv(TABLES / "table2_primary_sex_contrasts.csv", index=False)
sensitivities.to_csv(TABLES / "table3_sensitivity_models.csv", index=False)
table1.to_csv(TABLES / "table1_weighted_characteristics.csv", index=False)
ml.to_csv(TABLES / "table4_temporal_prediction_performance.csv", index=False)
incremental.to_csv(TABLES / "table5_incremental_dxa_value.csv", index=False)
components.to_csv(TABLES / "table6_component_sex_contrasts.csv", index=False)

colors = {"Men": "#0072B2", "Women": "#CC79A7"}
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "text.color": "black",
        "axes.labelcolor": "black",
        "axes.titlecolor": "black",
        "xtick.color": "black",
        "ytick.color": "black",
    }
)

fig, ax = plt.subplots(figsize=(7.2, 5.2))
for sex, subset in curve.groupby("sex"):
    subset = subset.sort_values("log_ltr_z")
    ax.plot(
        subset.log_ltr_z,
        subset.predicted_prevalence,
        label=sex,
        color=colors[sex],
        linewidth=2,
    )
    ax.fill_between(
        subset.log_ltr_z,
        subset.ci_low,
        subset.ci_high,
        color=colors[sex],
        alpha=0.18,
    )
ax.set(
    xlabel="Leg-to-trunk fat ratio, pooled standard-deviation units",
    ylabel="Adjusted prevalence of metabolic dysfunction",
)
ax.legend(frameon=False, title="Sex")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(FIGURES / "figure1_adjusted_association.svg")
fig.savefig(FIGURES / "figure1_adjusted_association.png", dpi=320)
plt.close(fig)

plot_contrasts = contrasts[contrasts.contrast.isin(["Men", "Women", "Interaction"])].copy()
plot_contrasts["display_label"] = plot_contrasts.contrast.replace(
    {"Interaction": "Sex interaction, ratio of PRs"}
)
fig, ax = plt.subplots(figsize=(7.2, 3.8))
y = np.arange(len(plot_contrasts))
ax.errorbar(
    plot_contrasts.prevalence_ratio,
    y,
    xerr=[
        plot_contrasts.prevalence_ratio - plot_contrasts.ci_low,
        plot_contrasts.ci_high - plot_contrasts.prevalence_ratio,
    ],
    fmt="o",
    color="#0072B2",
    ecolor="#4D4D4D",
    capsize=3,
)
ax.axvline(1, color="black", linestyle="--", linewidth=1)
ax.set_yticks(y, plot_contrasts.display_label)
ax.set_xlabel("Effect estimate (95% CI)")
ax.invert_yaxis()
ax.spines[["top", "right", "left"]].set_visible(False)
fig.tight_layout()
fig.savefig(FIGURES / "figure2_primary_forest.svg")
fig.savefig(FIGURES / "figure2_primary_forest.png", dpi=320)
plt.close(fig)

panel_order = ["A_base", "B_bmi", "C_bmi_waist", "D_dxa"]
model_order = ["penalized_logistic", "spline_logistic", "xgboost"]
fig, ax = plt.subplots(figsize=(7.2, 4.6))
width = 0.24
x = np.arange(len(panel_order))
model_colors = ["#0072B2", "#009E73", "#D55E00"]
for offset, (model, color) in enumerate(zip(model_order, model_colors)):
    model_rows = ml[ml.model == model].set_index("panel").loc[panel_order]
    values = model_rows.weighted_auc.to_numpy()
    yerr = np.vstack(
        [
            values - model_rows.auc_ci_low.to_numpy(),
            model_rows.auc_ci_high.to_numpy() - values,
        ]
    )
    model_label = "XGBoost" if model == "xgboost" else model.replace("_", " ")
    ax.bar(
        x + (offset - 1) * width,
        values,
        width,
        yerr=yerr,
        capsize=2,
        label=model_label,
        color=color,
        error_kw={"ecolor": "#4D4D4D", "elinewidth": 0.8},
    )
ax.set_xticks(x, ["Base", "+ BMI", "+ Waist", "+ DXA"])
ax.set_ylabel("Weighted temporal-test ROC AUC")
ax.set_ylim(max(0.5, ml.weighted_auc.min() - 0.05), min(1.0, ml.weighted_auc.max() + 0.05))
ax.legend(frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(FIGURES / "figure3_temporal_model_comparison.svg")
fig.savefig(FIGURES / "figure3_temporal_model_comparison.png", dpi=320)
plt.close(fig)

def contrast_text(name):
    row = contrasts[contrasts.contrast == name].iloc[0]
    return (
        f"PR {row.prevalence_ratio:.2f}, 95% CI {row.ci_low:.2f} to "
        f"{row.ci_high:.2f}, p={row.p_value:.3g}"
    )

best = ml.sort_values(["weighted_log_loss", "weighted_brier"]).iloc[0]
dx = incremental.set_index("model")

methods = f"""# Methods draft

## Study design and population

We conducted a repeated cross-sectional analysis of the 2011–2018 National Health and Nutrition Examination Survey. The target population comprised noninstitutionalized US adults aged 20–59 years. Participants were eligible if they completed the mobile examination, were not pregnant, had a positive fasting-subsample weight, valid regional dual-energy X-ray absorptiometry measurements, all four primary metabolic components, and complete prespecified covariates.

## Exposure and outcomes

The primary exposure was the natural logarithm of leg fat mass divided by trunk fat mass. It was standardized using one pooled, fasting-weighted standard deviation. The primary outcome was metabolic dysfunction, defined as at least two of elevated triglycerides, reduced high-density lipoprotein cholesterol, elevated blood pressure, and elevated fasting glucose, with public questionnaire treatment indicators incorporated. Conventional metabolic syndrome was a secondary outcome.

## Statistical analysis

We used the fasting-subsample weights divided by four for pooled 2011–2018 inference and accounted for masked strata and primary sampling units. The primary survey-weighted quasipoisson model included the exposure, sex, their interaction, age as a natural spline, race and ethnicity, survey cycle, education, poverty-income ratio, smoking, and total fat-mass index. We report prevalence ratios with 95% confidence intervals. Sensitivity analyses tested measured-only components, conventional metabolic syndrome, alternative adiposity adjustment, component fat models, and cycle exclusion. Associations with the four individual metabolic components were exploratory, with Benjamini-Hochberg control of the false-discovery rate for their interaction tests.

An exploratory prediction analysis compared penalized logistic regression, spline logistic regression, and XGBoost. Models were developed and tuned using 2011–2016 data and evaluated in 2017–2018, then rerun after documented data corrections without test-driven changes to candidate models. We assessed weighted discrimination, overall accuracy, and calibration. Deep learning was excluded a priori. As a publication-stage exploratory uncertainty analysis, 95% percentile intervals for ROC AUC and paired AUC differences were obtained from 1,000 bootstrap samples that used the Rao-Wu n_h−1 rescaled PSU subbootstrap within strata, conditional on the fitted models of the temporal holdout.
"""

results = f"""# Results draft

## Sample

The harmonized source contained {int(q['rows_all_cycles']):,} records. The primary complete-case population included {int(q['primary_complete']):,} participants, including {int(q['primary_women']):,} women and {int(q['primary_men']):,} men. Metabolic dysfunction was present in {int(q['primary_cases']):,} unweighted participants.

## Primary association

Per one pooled standard deviation higher log leg-to-trunk fat ratio, the adjusted association was {contrast_text('Men')} in men and {contrast_text('Women')} in women. The direct exposure-by-sex interaction was {contrast_text('Interaction')}. These estimates are cross-sectional associations and do not identify lipedema or establish protection.

## Temporal prediction

The best temporal-test model by weighted log loss was {best['model'].replace('_', ' ')} using the {best['panel']} panel (ROC AUC {best['weighted_auc']:.3f}, 95% cluster-bootstrap CI {best['auc_ci_low']:.3f} to {best['auc_ci_high']:.3f}; Brier score {best['weighted_brier']:.3f}; calibration slope {best['calibration_slope']:.3f}). Adding DXA variables to BMI and waist increased ROC AUC by {dx.loc['penalized_logistic', 'delta_auc_dxa_minus_bmi_waist']:+.3f} (95% paired cluster-bootstrap CI {dx.loc['penalized_logistic', 'delta_auc_ci_low']:.3f} to {dx.loc['penalized_logistic', 'delta_auc_ci_high']:.3f}) for penalized logistic regression and by {dx.loc['xgboost', 'delta_auc_dxa_minus_bmi_waist']:+.3f} for XGBoost. The full performance comparison is reported in Table 3.
"""

(REPORT_FRAGMENTS / "methods_summary.md").write_text(methods)
(REPORT_FRAGMENTS / "results_summary.md").write_text(results)
(FIGURES / "captions.md").write_text(
    """# Figure captions

## Figure 1

Adjusted prevalence of metabolic dysfunction across the pooled standardized leg-to-trunk fat-mass ratio in women and men. Lines show model estimates and shaded areas show 95% confidence intervals at the prespecified reference covariate profile. DXA, dual-energy X-ray absorptiometry.

## Figure 2

Survey-weighted prevalence ratios and 95% confidence intervals for the primary sex-specific exposure contrasts and direct interaction contrast. CI, confidence interval; PR, prevalence ratio.

## Figure 3

Weighted receiver operating characteristic area under the curve in the 2017–2018 temporal test sample for the prespecified feature panels and model classes. Error bars show 95% intervals from 1,000 bootstrap samples that used the Rao-Wu n_h−1 rescaled PSU subbootstrap within strata, conditional on the fitted models. AUC, area under the curve; BMI, body mass index; DXA, dual-energy X-ray absorptiometry; ROC, receiver operating characteristic.
"""
)

print("Publication report package built.")
