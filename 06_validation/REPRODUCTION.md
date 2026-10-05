# Reproduction check, 5 October 2026

The full pipeline completed in a fresh local Git clone with Python 3.12 and the recorded package versions, R 4.6.0 and survey 4.5. No original working-project outputs were overwritten. All 69 cached CDC source files were verified against frozen checksums. ALQ_G was additionally downloaded from CDC and checksum-verified. The other 68 files were not freshly downloaded during this check.

Data construction, association models, all prediction models, 1,000 bootstrap replicates, figures, tables, manuscript and supplement builds, and package validation passed. Primary n=3971; temporal-test n=751. Key numerical outputs agree within rtol=1e-9 and atol=1e-11; all displayed main and supplement table cells match the current paper. See reproduction.json.

This confirms a fresh checkout with recorded dependencies on this Mac. It is not a cross-platform test or proof of future URL availability. The R environment was supplied from an existing local library; r-installed-versions.csv records the full installed versions. Python dependencies were installed into a new isolated environment. The original Python 3.9.6 and the reproduced Python 3.12 environment are both documented.

Excluded from publication: raw records, derived participant rows, individual predictions, fitted binary models, internal reviews and prior document versions. Historical population comparison remains an explicitly non-regenerated aggregate artifact. Rights are reserved pending author selection of an open-source license.
