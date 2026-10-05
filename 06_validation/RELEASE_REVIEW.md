# Scientific and technical release review

Date: 5 October 2026. Scope: the publication repository and its associated manuscript source, supplement-building code, all reference aggregate outputs, source manifest, data construction, survey inference, temporal prediction and reproduction entry points. The review used the reviewer-2 framework and a separate technical checklist in the same assisted session. It is not independent human peer review or a security certification.

## Decision

Suitable for a versioned public research-code release after the checks below pass. No identified unresolved critical or major issue prevents that bounded release. This does not mean zero risk, complete journal compliance or absence of undiscovered bugs. The full pipeline was reproduced locally; source measurement accuracy, all potential confounders, cross-platform compatibility and full historical provenance cannot be proven by reproduction.

## Findings and disposition

### SCI-01: Model-dependent sex heterogeneity

Severity: major if presented as a consistent sex difference. Evidence: confirmed methodological limitation, already addressed. Anchors: manuscript Results and Discussion; primary_sex_contrasts.csv; nonlinear_interaction_test.csv; sensitivity_sex_contrasts.csv. The log-linear interaction supports a difference, whereas the full cubic interaction and conservative single-count lipid sensitivity do not establish a consistent sex difference. The main conclusion explicitly says a consistently stronger association in female participants was not established. Verification: direct interaction contrasts, their full covariance-based calculation, sensitivity outputs and their manuscript wording were checked. No new model was selected or fitted for this review. Residual: functional form and outcome definition remain consequential.

### SCI-02: Meaning of added discrimination

Severity: major if attributed to regional distribution alone. Evidence: confirmed potential misinterpretation, already addressed. Anchors: 03_ml_analysis.py panels C/D; manuscript Abstract, Results and Conclusion. Panel D adds total FMI as well as regional variables; the text explicitly attributes improvement to their joint addition. Temporal testing assesses contemporaneous classification, not future disease incidence. Verification: code-to-feature and outcome-time mapping; paired bootstrap differences. Residual: calibration and AUC do not establish clinical utility; intervals condition on fitted models and omit training uncertainty.

### SCI-03: Survey, missingness and endpoint construction

Severity: major limitation, disclosed rather than removable by packaging. Anchors: 01_build_dataset.R, data_rules.R, 02_survey_analysis.R and Supplementary Methods S1. Positive component findings take precedence over other missing inputs; four classifiable components are required. Generic lipid treatment may count twice; alternatives are reported. Fasting weights are divided by four; full fasting design precedes domain restriction. Primary strata do not overlap cycles; no education refusal/unknown codes occur in the primary sample. Verification: aggregate checks, synthetic medication tests and read-through of survey contrasts. Residual: complete-case and DXA selection, treatment misclassification, confounding and cross-sectional temporality prevent causal interpretation.

### TECH-01: Historical archive dependency

Severity: major reproducibility defect; confirmed and fixed. Anchor: 08_revision_supplement.py previously opened an internal baseline archive. Removed that dependency from the release. The historical population comparison remains a clearly labelled aggregate artifact, never an input to current estimates. Verification: full reproduction without that archive; 37 aggregate result/table files match the reference within rtol=1e-9 and atol=1e-11. Residual: the historical comparison itself is not regenerated.

### TECH-02: Stale output and overwrite hazards

Severity: major operational defect; confirmed and fixed. Anchor: the original shell entry point writes into its tree. Added run_reproduction.py, which refuses existing work directories and paths inside the release, checks the release inventory and dependencies, copies no reference analysis results, and writes completion only after the full pipeline and numerical comparison pass. Verification: failing tests before implementation, passing boundary tests afterwards, and a clean-work full run. The low-level entry point is retained for the isolated copy and explicitly documented. Residual: interrupted work remains for inspection; no automatic deletion or rollback is attempted.

### TECH-03: Package integrity and dependency limits

Severity: moderate; confirmed documentation/guard gap, fixed within tested scope. Added SHA-256 inventory verification, exact Python dependency checks, exact required R version checks, Git line-ending preservation, and source-checksum corruption tests. The downloader uses a uniquely named temporary file and never replaces an existing mismatching raw file. OSV query covered 24 pinned Python packages with no returned known advisory at the time of the check. This is not a complete vulnerability audit of R, system libraries or future advisories. R version inventory is not a tested from-source installer; the Python environment was freshly installed, the R library was pre-existing. These limitations are explicit in README and reproduction evidence.

### PUB-01: Authorship, AI support and publication scope

Severity: moderate if overstated; addressed. AI assistance is disclosed in the same support-based style as the existing public NHANES and HRS repositories, without claiming an unverified model name or independent human review. Code creation and scientific responsibility remain distinct. License remains rights-reserved pending author selection; this is public source access, not an open-source license. No source data, individual predictions, serialized fitted objects, secrets or internal reviews belong to the tracked inventory. Public working manuscript text is labelled as such. Patient/public involvement is still explicitly awaiting author confirmation and is not falsely declared complete.

## Evidence and boundaries

- Reproduction: primary n=3971, cases=1643; development n=3220, temporal test n=751. All main and supplementary displayed table cells matched in the initial clean-clone reproduction.
- New-run guard tests, bootstrap cluster tests and medication-rule synthetic tests are executable under tests/.
- Only ALQ_G was downloaded anew during the first check; the remaining 68 cached public source files were checksum-verified. The runner supports downloading all sources, but a full new download was not separately demonstrated.
- No new substantive statistical analysis, new endpoint, or data correction was introduced by this release review.
- Numerical reproduction does not independently verify every citation, all raw measurements or every source provenance claim. Prior reference checks are preserved; this release review did not repeat a complete literature review.

## Primary sources checked for applicability

- CDC weighting tutorial: https://wwwn.cdc.gov/nchs/nhanes/tutorials/weighting.aspx
- CDC questionnaire variable documentation: https://wwwn.cdc.gov/nchs/nhanes/search/variablelist.aspx?Component=Questionnaire
- TRIPOD+AI scope: https://www.tripod-statement.org/scope/
- Official 2024 checklist: https://www.tripod-statement.org/wp-content/uploads/2024/04/TRIPODAI-Supplement.pdf

### TECH-04: Obsolete helper table in the initial reference tree

Severity: moderate reproducibility defect; confirmed and fixed. Anchor: former 04_outputs/tables/table2_docx.csv. The initial fresh-clone check retained reference outputs and therefore did not demonstrate that every file was newly generated. The subsequent empty-output run caught this obsolete, unused helper table. It was removed from the supported release; current manuscript Table 2 uses table3_docx.csv and was unaffected. Verification: a new empty-output run regenerated and compared all 37 remaining aggregate CSVs successfully before release. Earlier reports of 38 matches are historical comparisons and are superseded by this stricter check. Residual: equality against reference outputs establishes numerical consistency, not independent methodological validity.

The code-availability paragraph and matching supplement statements now refer to the verified public GitHub repository and its v1.0.0 release. No DOI, permanent archival preservation or public binary-model access is claimed. The Word files in the separate manuscript workspace have not been changed by this repository release.
