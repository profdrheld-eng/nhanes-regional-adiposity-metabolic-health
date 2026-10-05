# NHANES regional adiposity and metabolic health

Analysis code for **Leg-to-trunk fat distribution and metabolic dysfunction beyond total adiposity in US adults: a repeated cross-sectional NHANES 2011–2018 study**.

Authors: Steffen Held, Florian Micke, Manuel Matzka and Eduard Isenmann.

The primary population includes 3,971 adults (1,643 cases). The exploratory prediction benchmark uses 3,220 development observations and 751 temporal-test observations. Cross-sectional associations do not establish causality or clinical utility. Sex heterogeneity depends on the exposure model. Added discrimination reflects both total and regional DXA variables.

## Reproduce

Use R 4.6.0 and Python 3.12 (the original analysis used Python 3.9.6; both software provenance records are retained). Install the exact Python dependencies into a dedicated environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r 03_analysis/environment/requirements-lock-python312.txt
```

Install the R packages specified in `03_analysis/environment/r-packages.txt` into an isolated R library. The `survey` version is 4.5; `foreign` is 0.8-91. Base package `splines` follows R. These are version specifications, not a complete transitive R lockfile.

```sh
.venv/bin/python 03_analysis/code/00_download_sources.py
PYTHON_BIN="$PWD/.venv/bin/python" sh 03_analysis/run_analysis.sh
```

If using a custom R library, set `R_LIBS_USER` to its location. `R_BIN` can select Rscript. The pipeline reads only local source files after download, rebuilds participant-level data, fits association and prediction models, computes 1,000 rescaled-bootstrap replicates, rebuilds tables/figures and documents, then validates the package. Runtime depends on the machine. Outputs are replaced during regeneration; preserve a release copy for comparison.

## Structure

- `01_project/analysis_plan`: local frozen plan and amendments; not independent preregistration.
- `02_data/manifests`: original CDC URLs, file sizes and checksums for 69 files.
- `03_analysis`: ordered R/Python scripts, configuration and dependency versions.
- `04_outputs`: aggregate reference results, tables and figures.
- `05_manuscript`: manuscript source, reporting checklists and bibliographic registry. These are working publication materials, not evidence of journal acceptance.
- `06_validation`: reproducibility evidence and release checks.

Raw records, derived participant-level data, individual predictions, fitted binary model files and internal review history are excluded from Git. The pipeline regenerates data and fitted models locally. `revision_population_comparison.csv` is a frozen aggregate historical comparison; its superseded individual-level source archive is not distributed and this historical comparison is not regenerated. It is not an input to current study estimates.

## Versions and citation

Cite the repository URL, release tag `v1.0.0` and full commit SHA. `CITATION.cff` supplies authorship metadata. This repository uses GitHub releases without Zenodo or a DOI. GitHub hosting and a release tag are not a guarantee of permanent archival preservation.

## Rights and limitations

Public source access is provided for inspection and reproducibility. An open-source reuse license has not been approved; see `LICENSE`. CDC data and third-party packages retain their own terms. These research models are not validated clinical tools. Patient/public involvement confirmation remains an author item in the reporting checklist.
