# NHANES regional adiposity and metabolic health

Analysis code for **Leg-to-trunk fat distribution and metabolic dysfunction beyond total adiposity in US adults: a repeated cross-sectional NHANES 2011–2018 study**.

Authors: Steffen Held, Florian Micke, Manuel Matzka and Eduard Isenmann.

The primary population includes 3,971 adults (1,643 cases). The exploratory prediction benchmark uses 3,220 development observations and 751 temporal-test observations. Cross-sectional associations do not establish causality or clinical utility. Sex heterogeneity depends on the exposure model. Added discrimination reflects both total and regional DXA variables.

## Reproduce safely

The tested runtime is R 4.6.0 and Python 3.12. The original analysis used Python 3.9.6; the current numerical reproduction is documented separately. Install dependencies in an environment outside the repository:

```sh
python3.12 -m venv /your/local/adiposity-env
/your/local/adiposity-env/bin/python -m pip install -r 03_analysis/environment/requirements-lock-python312.txt
```

`03_analysis/environment/r-required-versions.csv` lists the exact R dependency closure used here. Install these versions in an isolated R library; set `R_LIBS_USER` to its location. This list is not an installer or a transitive source-archive lockfile. No command here installs packages automatically. macOS was tested; Windows and Linux runtime support has not been demonstrated.

```sh
/your/local/adiposity-env/bin/python -B verify_release.py
/your/local/adiposity-env/bin/python -B -m unittest discover -s tests -v
Rscript --vanilla tests/test_data_rules.R
/your/local/adiposity-env/bin/python -B run_reproduction.py --work-dir /your/new/adiposity-work
```

The work directory must not exist and must be outside this repository. The runner checks dependency versions, creates an isolated copy without the reference results, downloads the public CDC inputs, verifies all 69 source checksums, runs all analysis and reporting stages, and compares 37 aggregate result/table files against the release. Only the explicitly documented historical aggregate is copied. It writes `pipeline_complete.json` only after every step succeeds. A failed run leaves its log and partial outputs for inspection; use a new directory for another attempt.

To use existing public files, add `--data-dir /your/local/nhanes-xpt`; they are copied and verified before analysis. No existing input file is changed. Do not upload the work directory: it contains individual records, predictions and fitted objects. The low-level `03_analysis/run_analysis.sh` is for the isolated work copy; use the top-level runner for normal reproduction. Runtime depends on the machine.

## Structure

- `01_project/analysis_plan`: local frozen plan and amendments; not independent preregistration.
- `02_data/manifests`: original CDC URLs, file sizes and checksums for 69 files.
- `03_analysis`: ordered R/Python scripts, configuration and dependency versions.
- `04_outputs`: aggregate reference results, tables and figures.
- `05_manuscript`: manuscript source, reporting checklists and bibliographic registry. These are working publication materials, not evidence of journal acceptance.
- `06_validation`: reproducibility evidence and release checks.

Raw records, derived participant-level data, individual predictions, fitted binary model files and internal review history are excluded from Git. The pipeline regenerates data and fitted models locally. `revision_population_comparison.csv` is a frozen aggregate historical comparison; its superseded individual-level source archive is not distributed and this historical comparison is not regenerated. It is not an input to current study estimates.

## Versions and citation

The numerical analysis release remains `v1.0.0`. Subsequent commits synchronize publication statements with the current manuscript without changing analysis code or reference estimates. Cite the repository URL, the release tag and its full commit SHA for the analysis; cite the exact later commit separately when referring to updated publication statements. `CITATION.cff` supplies authorship metadata. This repository uses GitHub releases without Zenodo or a DOI. GitHub hosting and a release tag are not a guarantee of permanent archival preservation.

## Rights and limitations

Public source access is provided for inspection and reproducibility. An open-source reuse license has not been approved; see `LICENSE`. CDC data and third-party packages retain their own terms. These research models are not validated clinical tools. The author confirmed that there was no patient involvement in this secondary analysis.

## AI assistance and author responsibility

OpenAI Codex assisted with code development, debugging, explanatory documentation, language editing and reproducibility checks. This support does not establish the validity of methodological assumptions or replace scientific judgment. The authors retain responsibility for analytical decisions, interpretation and the released materials. Participant-level computations were executed locally; the public release contains aggregate outputs rather than participant records. No AI system is listed as an author.

## Review and remaining limits

The release audit is documented in `06_validation/RELEASE_REVIEW.md`. Tests do not guarantee error-free code or risk-free use. No known unresolved release-blocking issue was identified in the documented review. This is a research-code release, not a declaration that the associated manuscript is submission-ready. Final journal-specific checks remain a separate publication task. Restoring the full R dependency set into a new empty library has not yet been demonstrated; the existing numerical reproduction used an available R library.
