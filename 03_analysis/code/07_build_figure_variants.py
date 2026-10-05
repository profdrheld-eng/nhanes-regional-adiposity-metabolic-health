#!/usr/bin/env python3
"""Build publication-facing figure variants from frozen analysis outputs."""

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
FIGURES = PROJECT / "04_outputs" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

SEX_COLORS = {"Male": "#5BB6C4", "Female": "#D98F8A"}
MODEL_COLORS = {
    "penalized_logistic": "#E7AAA6",
    "spline_logistic": "#82CBCD",
    "xgboost": "#B5A2D1",
}
MODEL_LABELS = {
    "penalized_logistic": "Penalized logistic",
    "spline_logistic": "Spline logistic",
    "xgboost": "XGBoost",
}
PANEL_ORDER = ["A_base", "B_bmi", "C_bmi_waist", "D_dxa"]
PANEL_LABELS = ["Base", "+ BMI", "+ Waist", "+ DXA"]
MODEL_ORDER = list(MODEL_COLORS)


plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "font.weight": "bold",
        "axes.labelweight": "bold",
        "axes.titleweight": "bold",
        "text.color": "black",
        "axes.labelcolor": "black",
        "axes.titlecolor": "black",
        "xtick.color": "black",
        "ytick.color": "black",
    }
)


def bold_axes(ax):
    for label in [*ax.get_xticklabels(), *ax.get_yticklabels()]:
        label.set_fontweight("bold")
    ax.xaxis.label.set_fontweight("bold")
    ax.yaxis.label.set_fontweight("bold")


def bold_legend(legend):
    if legend is None:
        return
    for text in legend.get_texts():
        text.set_fontweight("bold")


def save_figure(fig, stem, aliases=()):
    fig.tight_layout()
    for output_stem in (stem, *aliases):
        fig.savefig(FIGURES / f"{output_stem}.svg", bbox_inches="tight")
        fig.savefig(FIGURES / f"{output_stem}.png", dpi=320, bbox_inches="tight")
    plt.close(fig)


def add_standardized_bands(ax):
    ax.axvspan(-0.5, 0.5, color="#BDBDBD", alpha=0.28, zorder=0)
    ax.axvspan(-1.5, -0.5, color="#D9D9D9", alpha=0.22, zorder=0)
    ax.axvspan(0.5, 1.5, color="#D9D9D9", alpha=0.22, zorder=0)
    ax.axvspan(-3.0, -1.5, color="#F0F0F0", alpha=0.18, zorder=0)
    ax.axvspan(1.5, 3.0, color="#F0F0F0", alpha=0.18, zorder=0)
    ax.axvline(0, color="#666666", linewidth=1.5, linestyle="--", zorder=1)


def build_figure1(curve, stem, banded):
    fig, ax = plt.subplots(figsize=(7.4, 5.3))
    if banded:
        add_standardized_bands(ax)
    for source_label, display_label in (("Men", "Male"), ("Women", "Female")):
        subset = curve[curve.sex == source_label].sort_values("log_ltr_z")
        color = SEX_COLORS[display_label]
        ax.fill_between(
            subset.log_ltr_z,
            subset.ci_low,
            subset.ci_high,
            color=color,
            alpha=0.17,
            linewidth=0,
            zorder=2,
        )
        ax.plot(
            subset.log_ltr_z,
            subset.predicted_prevalence,
            label=display_label,
            color=color,
            linewidth=3.4,
            zorder=3,
        )
    ax.set_xlim(-2.0, 2.0)
    ax.margins(x=0)
    ax.set_xlabel("Log leg-to-trunk fat ratio, pooled SD units")
    ax.set_ylabel("Fitted prevalence, log-linear exposure model")
    legend = ax.legend(frameon=False, loc="upper right")
    bold_legend(legend)
    bold_axes(ax)
    ax.spines[["top", "right"]].set_visible(False)
    aliases = ("figure1_adjusted_association",) if banded else ()
    save_figure(fig, stem, aliases=aliases)


def add_pr_bands(ax):
    bands = [
        (0.50, 0.65, "#F2F2F2", 0.55),
        (0.65, 0.80, "#D9D9D9", 0.38),
        (0.80, 1.00, "#BDBDBD", 0.28),
        (1.00, 1.28, "#F2F2F2", 0.45),
    ]
    for left, right, color, alpha in bands:
        ax.axvspan(left, right, color=color, alpha=alpha, zorder=0)
    ax.axvline(1, color="#4D4D4D", linestyle="--", linewidth=1.7, zorder=1)


def format_p(value):
    if value < 0.001:
        return "p < 0.001"
    return f"p = {value:.3f}"


def build_figure2(contrasts):
    plot_rows = contrasts[contrasts.contrast.isin(["Men", "Women", "Interaction"])].copy()
    plot_rows["display_label"] = plot_rows.contrast.map(
        {
            "Men": "Male",
            "Women": "Female",
            "Interaction": "Female-to-male ratio of PRs",
        }
    )
    plot_rows["display_color"] = plot_rows.contrast.map(
        {
            "Men": SEX_COLORS["Male"],
            "Women": SEX_COLORS["Female"],
            "Interaction": "#4D4D4D",
        }
    )
    fig, ax = plt.subplots(figsize=(10.2, 4.0))
    add_pr_bands(ax)
    y = np.array([0.20, 1.00, 1.80])
    for ypos, row in zip(y, plot_rows.itertuples(index=False)):
        ax.hlines(
            ypos,
            row.ci_low,
            row.ci_high,
            color=row.display_color,
            linewidth=3.2,
            zorder=3,
        )
        ax.scatter(
            row.prevalence_ratio,
            ypos,
            s=105,
            color=row.display_color,
            edgecolor="white",
            linewidth=0.8,
            zorder=4,
        )
        ax.text(
            1.025,
            ypos,
            (
                f"{row.prevalence_ratio:.2f} "
                f"({row.ci_low:.2f}–{row.ci_high:.2f}), "
                f"{format_p(row.p_value)}"
            ),
            va="center",
            ha="left",
            fontweight="bold",
            fontsize=9.5,
            color="black",
        )
    ax.set_xlim(0.50, 1.28)
    ax.set_yticks(y, plot_rows.display_label)
    ax.set_xlabel("Prevalence ratio (95% confidence interval)")
    ax.invert_yaxis()
    ax.set_ylim(2.05, -0.05)
    bold_axes(ax)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    save_figure(
        fig,
        "figure2_variant_banded_estimates",
        aliases=("figure2_primary_forest",),
    )


def auc_error(model_rows):
    values = model_rows.weighted_auc.to_numpy()
    errors = np.vstack(
        [
            values - model_rows.auc_ci_low.to_numpy(),
            model_rows.auc_ci_high.to_numpy() - values,
        ]
    )
    return values, errors


def add_auc_bands_vertical(ax):
    for low, high, color, alpha in [
        (0.50, 0.60, "#F2F2F2", 0.55),
        (0.60, 0.70, "#D9D9D9", 0.36),
        (0.70, 0.80, "#F2F2F2", 0.55),
        (0.80, 0.90, "#D9D9D9", 0.36),
    ]:
        ax.axhspan(low, high, color=color, alpha=alpha, zorder=0)
    ax.axhline(0.50, color="#666666", linestyle="--", linewidth=1.4, zorder=1)


def add_auc_bands_horizontal(ax):
    for low, high, color, alpha in [
        (0.50, 0.60, "#F2F2F2", 0.55),
        (0.60, 0.70, "#D9D9D9", 0.36),
        (0.70, 0.80, "#F2F2F2", 0.55),
        (0.80, 0.90, "#D9D9D9", 0.36),
    ]:
        ax.axvspan(low, high, color=color, alpha=alpha, zorder=0)
    ax.axvline(0.50, color="#666666", linestyle="--", linewidth=1.4, zorder=1)


def build_figure3_vertical(ml):
    fig, ax = plt.subplots(figsize=(7.5, 5.0))
    add_auc_bands_vertical(ax)
    width = 0.24
    x = np.arange(len(PANEL_ORDER))
    for offset, model in enumerate(MODEL_ORDER):
        rows = ml[ml.model == model].set_index("panel").loc[PANEL_ORDER]
        values, errors = auc_error(rows)
        color = MODEL_COLORS[model]
        ax.bar(
            x + (offset - 1) * width,
            values,
            width,
            yerr=errors,
            capsize=4,
            label=MODEL_LABELS[model],
            color=color,
            alpha=0.96,
            zorder=3,
            error_kw={"ecolor": color, "elinewidth": 2.5, "capthick": 2.5},
        )
    ax.set_xticks(x, PANEL_LABELS)
    ax.set_ylabel("Weighted temporal-test ROC AUC")
    ax.set_ylim(0.50, 0.88)
    legend = ax.legend(frameon=False, loc="upper left")
    bold_legend(legend)
    bold_axes(ax)
    ax.spines[["top", "right"]].set_visible(False)
    save_figure(fig, "figure3_variant_vertical_banded")


def build_figure3_horizontal(ml):
    fig, ax = plt.subplots(figsize=(7.7, 5.2))
    add_auc_bands_horizontal(ax)
    height = 0.22
    y = np.arange(len(PANEL_ORDER))
    for offset, model in enumerate(MODEL_ORDER):
        rows = ml[ml.model == model].set_index("panel").loc[PANEL_ORDER]
        values, errors = auc_error(rows)
        color = MODEL_COLORS[model]
        ax.barh(
            y + (offset - 1) * height,
            values,
            height,
            xerr=errors,
            capsize=4,
            label=MODEL_LABELS[model],
            color=color,
            alpha=0.96,
            zorder=3,
            error_kw={"ecolor": color, "elinewidth": 2.5, "capthick": 2.5},
        )
    ax.set_yticks(y, PANEL_LABELS)
    ax.set_xlabel("Weighted temporal-test ROC AUC")
    ax.set_xlim(0.50, 0.88)
    ax.invert_yaxis()
    legend = ax.legend(
        frameon=False,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.01),
        ncol=3,
    )
    bold_legend(legend)
    bold_axes(ax)
    ax.spines[["top", "right"]].set_visible(False)
    save_figure(
        fig,
        "figure3_variant_horizontal_banded",
        aliases=("figure3_temporal_model_comparison",),
    )


def main():
    curve = pd.read_csv(RESULTS / "adjusted_prediction_curve.csv")
    contrasts = pd.read_csv(RESULTS / "primary_sex_contrasts.csv")
    ml = pd.read_csv(RESULTS / "ml_temporal_metrics.csv")
    build_figure1(curve, "figure1_variant_clean", banded=False)
    build_figure1(curve, "figure1_variant_banded", banded=True)
    build_figure2(contrasts)
    build_figure3_vertical(ml)
    build_figure3_horizontal(ml)
    print("Built 5 publication figure variants.")


if __name__ == "__main__":
    main()
