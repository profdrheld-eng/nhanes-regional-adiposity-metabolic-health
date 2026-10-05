#!/bin/sh
set -eu

analysis_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
r_bin=${R_BIN:-Rscript}
python_bin=${PYTHON_BIN:-python3}
docx_python=${DOCX_PYTHON_BIN:-$python_bin}

"$r_bin" "$analysis_dir/code/01_build_dataset.R"
"$r_bin" "$analysis_dir/code/02_survey_analysis.R"
"$python_bin" "$analysis_dir/code/03_ml_analysis.py"
"$python_bin" "$analysis_dir/code/04_build_report.py"
"$python_bin" "$analysis_dir/code/07_build_figure_variants.py"
"$python_bin" "$analysis_dir/code/08_revision_supplement.py"
"$python_bin" "$analysis_dir/code/10_build_participant_flow.py"
"$docx_python" "$analysis_dir/code/06_build_manuscript_docx.py"
"$docx_python" "$analysis_dir/code/09_build_supplement_docx.py"
"$python_bin" "$analysis_dir/code/05_validate_package.py"
