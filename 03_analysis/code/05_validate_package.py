#!/usr/bin/env python3
"""Fail-closed validation of lineage, model outputs, reports, and figures."""

import hashlib
import re
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DERIVED = ROOT / "02_data" / "derived"
MANIFESTS = ROOT / "02_data" / "manifests"
RESULTS = ROOT / "04_outputs" / "results"
FIGURES = ROOT / "04_outputs" / "figures"
MANUSCRIPT = ROOT / "05_manuscript" / "source"
QUALITY_CONTROL = ROOT / "05_manuscript" / "quality_control"
REPORT_FRAGMENTS = ROOT / "04_outputs" / "report_fragments"
SOURCE_RAW = ROOT / "02_data" / "raw_public"

required = [
    ROOT / "01_project" / "analysis_plan" / "analysis-plan.md",
    ROOT / "03_analysis" / "config" / "frozen-analysis.json",
    MANIFESTS / "source_manifest.csv",
    DERIVED / "harmonized_analysis_data.csv",
    RESULTS / "data_quality_checks.csv",
    RESULTS / "table1_publication.csv",
    RESULTS / "primary_sex_contrasts.csv",
    RESULTS / "sensitivity_model_coefficients.csv",
    RESULTS / "secondary_component_sex_contrasts.csv",
    RESULTS / "ml_temporal_metrics.csv",
    RESULTS / "ml_temporal_auc_bootstrap.csv",
    RESULTS / "ml_bootstrap_auc_replicates.csv",
    RESULTS / "ml_incremental_value.csv",
    DERIVED / "protected_test_predictions.csv",
    FIGURES / "figure1_adjusted_association.svg",
    FIGURES / "figure1_adjusted_association.png",
    FIGURES / "figure2_primary_forest.svg",
    FIGURES / "figure3_temporal_model_comparison.svg",
    FIGURES / "figure3_temporal_model_comparison.png",
    REPORT_FRAGMENTS / "methods_summary.md",
    REPORT_FRAGMENTS / "results_summary.md",
    MANUSCRIPT / "manuscript.md",
    QUALITY_CONTROL / "references_verified.csv",
    QUALITY_CONTROL / "strobe-cross-sectional-checklist.md",
]
missing = [str(path) for path in required if not path.exists() or path.stat().st_size == 0]
if missing:
    raise RuntimeError(f"Missing or empty required artifacts: {missing}")

source_manifest = pd.read_csv(MANIFESTS / "source_manifest.csv")
if len(source_manifest) != 69:
    raise RuntimeError("Expected 69 source files in the frozen NHANES manifest.")
for row in source_manifest.itertuples(index=False):
    source_path = SOURCE_RAW / row.file
    if not source_path.exists() or source_path.stat().st_size != row.bytes:
        raise RuntimeError(f"Missing or size-mismatched source file: {source_path}")
    if hashlib.md5(source_path.read_bytes()).hexdigest() != row.md5:
        raise RuntimeError(f"MD5 mismatch in source file: {source_path}")

data = pd.read_csv(DERIVED / "harmonized_analysis_data.csv", low_memory=False)
if data.SEQN.duplicated().any():
    raise RuntimeError("Duplicate SEQN in harmonized data.")
domain = data.primary_domain.astype(str).str.lower().eq("true")
if domain.sum() < 1000:
    raise RuntimeError("Implausibly small primary domain.")
if data.loc[domain, "sex"].nunique() != 2:
    raise RuntimeError("Both sexes are not represented in the primary domain.")
if (data.loc[domain, "pooled_fasting_weight"] <= 0).any():
    raise RuntimeError("Nonpositive primary survey weight.")

contrasts = pd.read_csv(RESULTS / "primary_sex_contrasts.csv")
if set(contrasts.contrast) != {"Men", "Women", "Interaction"}:
    raise RuntimeError("Primary contrast set is incomplete.")
if not np.isfinite(contrasts[["prevalence_ratio", "ci_low", "ci_high", "p_value"]]).all().all():
    raise RuntimeError("Nonfinite primary estimate.")
if (contrasts.ci_low > contrasts.prevalence_ratio).any() or (
    contrasts.ci_high < contrasts.prevalence_ratio
).any():
    raise RuntimeError("Invalid primary confidence interval.")

metrics = pd.read_csv(RESULTS / "ml_temporal_metrics.csv")
if len(metrics) != 12:
    raise RuntimeError("Expected 12 prespecified ML model-panel results.")
if not metrics.weighted_auc.between(0, 1).all():
    raise RuntimeError("Invalid ML AUC.")
if not metrics[["auc_ci_low", "auc_ci_high"]].apply(
    lambda column: column.between(0, 1).all()
).all():
    raise RuntimeError("Invalid bootstrap AUC confidence interval.")
if (metrics.auc_ci_low > metrics.weighted_auc).any() or (
    metrics.auc_ci_high < metrics.weighted_auc
).any():
    raise RuntimeError("Bootstrap AUC confidence interval excludes its point estimate.")
predictions = pd.read_csv(DERIVED / "protected_test_predictions.csv")
probability_columns = [c for c in predictions if "__" in c]
if len(probability_columns) != 12:
    raise RuntimeError("Protected test prediction matrix is incomplete.")
if predictions[probability_columns].isna().any().any():
    raise RuntimeError("Missing protected test probability.")
if not ((predictions[probability_columns] >= 0) & (predictions[probability_columns] <= 1)).all().all():
    raise RuntimeError("Protected test probability outside [0,1].")

for path in (
    REPORT_FRAGMENTS / "methods_summary.md",
    REPORT_FRAGMENTS / "results_summary.md",
):
    text = path.read_text()
    if "TODO" in text or "TBD" in text or len(text.split()) < 100:
        raise RuntimeError(f"Incomplete manuscript artifact: {path}")

manuscript_text = (MANUSCRIPT / "manuscript.md").read_text()
if "## Abstract" not in manuscript_text or "## Keywords" not in manuscript_text:
    raise RuntimeError("Structured abstract boundaries are missing.")
abstract_text = manuscript_text.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
abstract_words = len(re.findall(r"\b[\w'-]+\b", abstract_text))
if abstract_words > 250:
    raise RuntimeError(f"Abstract exceeds 250 words: {abstract_words}")
for prohibited in ("diagnoses lipedema", "protective effect", "causes lower"):
    if prohibited in manuscript_text.lower():
        raise RuntimeError(f"Prohibited overclaim in manuscript: {prohibited}")

references = pd.read_csv(QUALITY_CONTROL / "references_verified.csv", dtype=str).fillna("")
required_reference_fields = {
    "key",
    "first_author",
    "year",
    "title",
    "journal",
    "doi",
    "url",
    "verification",
}
if not required_reference_fields.issubset(references.columns):
    raise RuntimeError("Verified-reference registry is missing required fields.")
nonblank_dois = references.loc[references.doi != "", "doi"].str.lower()
nonblank_urls = references.loc[references.url != "", "url"].str.lower()
if (
    references.key.duplicated().any()
    or nonblank_dois.duplicated().any()
    or nonblank_urls.duplicated().any()
):
    raise RuntimeError("Duplicate key or DOI in verified-reference registry.")
if (
    references[
        ["key", "first_author", "year", "title", "journal", "verification"]
    ]
    == ""
).any().any():
    raise RuntimeError("Incomplete required metadata in verified-reference registry.")
if ((references.doi == "") & (references.url == "")).any():
    raise RuntimeError("Each verified reference requires a DOI or stable URL.")
doi_pattern = re.compile(r"https://doi\.org/(10\.\d{4,9}/\S+)", re.IGNORECASE)
manuscript_dois = {
    match.rstrip(".,;").lower() for match in doi_pattern.findall(manuscript_text)
}
registered_dois = set(nonblank_dois)
unregistered_dois = sorted(manuscript_dois - registered_dois)
if unregistered_dois:
    raise RuntimeError(f"Manuscript DOI absent from verified registry: {unregistered_dois}")

incremental = pd.read_csv(RESULTS / "ml_incremental_value.csv").set_index("model")
full_dxa = metrics[
    (metrics.panel == "D_dxa") & (metrics.model == "penalized_logistic")
].iloc[0]
required_numeric_claims = [
    f"{contrasts.iloc[0].prevalence_ratio:.2f} (95% confidence interval [CI], {contrasts.iloc[0].ci_low:.2f} to {contrasts.iloc[0].ci_high:.2f})",
    f"{contrasts.iloc[1].prevalence_ratio:.2f} (95% CI, {contrasts.iloc[1].ci_low:.2f} to {contrasts.iloc[1].ci_high:.2f})",
    f"{contrasts.iloc[2].prevalence_ratio:.2f} (95% CI, {contrasts.iloc[2].ci_low:.2f} to {contrasts.iloc[2].ci_high:.2f}",
    (
        f"{full_dxa.weighted_auc:.3f} (95% cluster-bootstrap CI, "
        f"{full_dxa.auc_ci_low:.3f} to {full_dxa.auc_ci_high:.3f})"
    ),
    (
        f"{incremental.loc['penalized_logistic', 'delta_auc_dxa_minus_bmi_waist']:.3f} "
        f"(95% paired cluster-bootstrap CI, "
        f"{incremental.loc['penalized_logistic', 'delta_auc_ci_low']:.3f} "
        f"to {incremental.loc['penalized_logistic', 'delta_auc_ci_high']:.3f})"
    ),
]
for claim in required_numeric_claims:
    if claim not in manuscript_text:
        raise RuntimeError(f"Manuscript is not synchronized with result files: {claim}")

rows = []
for path in sorted(p for p in ROOT.rglob("*") if p.is_file() and p.name != "artifact_manifest_sha256.csv" and not any(x in p.parts for x in (".git", ".venv", ".Rlibrary", "06_reviews", "07_revision", "99_archive", "__pycache__", "matplotlib-cache"))):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    rows.append(
        {
            "path": str(path.relative_to(ROOT)),
            "bytes": path.stat().st_size,
            "sha256": digest,
        }
    )
QUALITY_CONTROL.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows).to_csv(QUALITY_CONTROL / "artifact_manifest_sha256.csv", index=False)
print(
    f"PASS: validated {len(rows)} artifacts; primary n={domain.sum()}, "
    f"test n={len(predictions)}, abstract words={abstract_words}, "
    f"verified references={len(references)}"
)
