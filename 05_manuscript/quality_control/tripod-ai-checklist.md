# TRIPOD+AI reporting map

The prediction component is an exploratory contemporaneous benchmark. All checklist items are mapped below using stable section and object references. M = Manuscript; S = Supplementary File. This map does not certify full compliance; partial reporting and analyses not conducted remain explicit.

Official checklist: https://www.tripod-statement.org/wp-content/uploads/2019/12/TRIPODAI_checklist.pdf

| Item | Topic | Location | Assessment and limitations |
|---|---|---|---|
| 1 | Title | M Title and Abstract | Partial: prediction is secondary and not explicit in the title. |
| 2 | Abstract | M Abstract | Partial: test sample and results reported; development cases and a separate full abstract-checklist assessment remain absent. |
| 3a | Context | M Introduction | Clinical background and additional information beyond anthropometry described. |
| 3b | Intended use | M Introduction; S Methods S1–S2 | Research benchmark; no clinical deployment or prospective risk claim. |
| 4 | Objectives | M Introduction | Exploratory incremental discrimination from total and regional DXA measures jointly and model-class comparison specified. |
| 5a | Source | M Study Design | Public NHANES examinations identified. |
| 5b | Dates | M Study Design; S Table S9b | Development 2011–2016 and testing 2017–2018. |
| 6a | Setting | M Study Design | US noninstitutionalized civilian population. |
| 6b | Eligibility | M Study Population; S Table S3, Figure S3 | Complete-case selection and DXA eligibility stated. |
| 6c | Treatments | M Metabolic outcomes; S Table S4b | Treatment indicators incorporated in endpoint; no intervention assigned. |
| 7 | Preparation | M Data Preparation; S Methods S1–S2 | Linking, coding, exclusions and transformations reported. |
| 8a | Outcome | M Metabolic outcomes; S Methods S1 | Pragmatic contemporaneous endpoint defined. |
| 8b | Assessment | S Methods S1 | Public measurements and questionnaires; no additional adjudication or analyst blinding. |
| 9a | Predictors | M Prediction analysis; S Methods S2 | Four nested panels listed. |
| 9b | Measurement | S Methods S1–S2 | Source codes, units and transformations stated. |
| 9c | Subjectivity | S Methods S1 | No new subjective predictor assessment; existing public measurements used. |
| 10 | Size | M Study Population; S Methods S2 | Fixed eligible dataset; no formal model-development sample-size calculation. |
| 11 | Missingness | M Data Preparation; S Tables S4 and S8 | Initial complete-case selection and fold-specific imputation distinguished. |
| 12a | Partition | M Prediction analysis; S Table S9b | Temporal split and three cycle-based development folds stated. |
| 12b | Transformations | S Methods S2 | Scaling, imputation, one-hot encoding and splines specified. |
| 12c | Development | S Methods S2, Tables S9–S10 | Full candidate grid, selection rule and chosen parameters reported. |
| 12d | Clustering | M Prediction analysis; S Methods S2 | Cycle-based validation and within-stratum PSU bootstrap; no additional site model. |
| 12e | Performance | M Table 3; S Table S11, Figure S2 | Discrimination, scores and calibration; no clinical utility analysis. |
| 12f | Updating | S Methods S2 | No holdout recalibration or model updating. |
| 12g | Computation | S Methods S2; M Code availability | Fitted pipelines can be regenerated using the released code; binary models are not distributed. |
| 13 | Class balance | S Methods S2 | No synthetic balancing or over-/undersampling; survey weights used. |
| 14 | Fairness | S Methods S2 | No fairness analysis or fairness claim. |
| 15 | Output | S Methods S2 | Probabilities; no clinical decision threshold. |
| 16 | Differences | S Table S8 | Development and test distributions compared. |
| 17 | Ethics | M Ethics statement | Original survey consent and NCHS oversight; local determination confirmed by authors. |
| 18a | Funding | M Funding | No specific funding, as confirmed by authors. |
| 18b | Interests | M Conflicts of interest | None declared by authors. |
| 18c | Protocol | M Software and reproducibility | Local plan and dated amendment; permanent external access remains pending. |
| 18d | Registration | M Software and reproducibility | Local freezing is not independent preregistration. |
| 18e | Data | M Data availability | Public CDC data and local source manifest. |
| 18f | Code | M Code availability | Versioned GitHub code release available; no separate DOI or archival preservation service. |
| 19 | Public involvement | S Transparency | Author confirmation remains pending. |
| 20a | Flow | S Figure S3, Tables S3 and S8 | Counts, cases and noncases reported; no follow-up interval. |
| 20b | Description | M Table 1; S Tables S4b and S8 | Characteristics, medication and missingness described. |
| 20c | Comparison | S Table S8 | Development/test sample characteristics. |
| 21 | Analysis counts | S Tables S6b and S9b | Counts per cycle, fold and analysis. |
| 22 | Full model | S Table S10, Methods S2 | Partial: twelve fitted pipelines are generated by the released code; binary fitted objects are not distributed. |
| 23a | Uncertainty | M Table 3; S Tables S2 and S11, Figure S2 | Partial: AUC, delta-AUC and calibration intervals; other scores descriptive without intervals, no subgroup performance analysis. |
| 23b | Cluster variation | S Table S9 | Cycle-fold losses provided; no additional cluster-heterogeneity analysis. |
| 24 | Updating results | S Methods S2 | Not applicable, no updating performed. |
| 25 | Interpretation | M Discussion | Exploratory model comparisons; no proven superiority, equivalence or clinical utility. |
| 26 | Limitations | M Discussion | Selection, model form, modest temporal sample and conditional uncertainty disclosed. |
| 27a | Inputs in practice | S Methods S1–S2 | Not applicable, no deployment proposed. |
| 27b | User interaction | S Methods S1–S2 | Not applicable, research benchmark. |
| 27c | Further evaluation | M Discussion, final paragraph | Independent replication and clinical evaluation needed. |
