> Revision notice, 2026-10-05: The original plan below is retained. The authorized correction amendment is documented in `../../07_revision/2026-10-05/PLAN.md`. Local plan freezing is not independent preregistration.

# Frozen statistical analysis plan

## Identification

- Study ID: NHANES-LBF-MET-2026-01
- Frozen: 2026-07-26, before exposure-outcome modelling
- Design: repeated cross-sectional complex survey
- Population: US noninstitutionalized adults aged 20–59 years represented by NHANES 2011–2018
- Reporting: STROBE for the association analysis and TRIPOD+AI for the exploratory prediction analysis

## Paper vision

At comparable total adiposity, a more lower-body-predominant fat distribution is expected to be associated with lower metabolic burden, particularly in women, and regional DXA measures may add information beyond BMI and waist circumference.

## Research question and estimand

The primary question is whether a one pooled-survey-weighted standard deviation higher log leg-to-trunk fat-mass ratio is associated with the prevalence of non-anthropometric metabolic dysfunction and whether this association differs between women and men.

The primary estimand is the adjusted prevalence ratio with 95% confidence interval from one pooled exposure-by-sex interaction model. Sex-specific exposure contrasts use the same pooled standard deviation. Interpretation is associational, not causal.

## Population

Participants must:

1. be MEC-examined;
2. be aged 20–59 years;
3. have a positive fasting-subsample weight;
4. not be pregnant at examination;
5. have valid positive left-leg, right-leg, trunk, and total DXA fat mass;
6. have all four primary metabolic components observed;
7. have the prespecified primary covariates observed.

The survey design is constructed before defining the analysis domain. Pooled fasting weights are `WTSAF2YR / 4`; masked strata and PSU variables are `SDMVSTRA` and `SDMVPSU`.

## Exposure

Primary exposure:

`log((left leg fat + right leg fat) / trunk fat)`

It is standardized once using the pooled analytic population and fasting weights. Higher values indicate more leg relative to trunk fat.

Required alternative exposure analyses:

- leg and trunk fat mass entered separately as height-indexed variables;
- released android-to-gynoid ratio;
- visceral adipose tissue mass;
- BMI in place of total fat-mass index.

## Outcomes

Primary binary outcome, non-anthropometric metabolic dysfunction, is at least two of:

1. triglycerides at least 150 mg/dL or reported cholesterol medication;
2. HDL cholesterol below 40 mg/dL in men or 50 mg/dL in women, or reported cholesterol medication;
3. mean systolic blood pressure at least 130 mmHg, mean diastolic blood pressure at least 85 mmHg, or antihypertensive treatment;
4. fasting glucose at least 100 mg/dL, diagnosed diabetes, insulin, or oral diabetes medication.

All four components must be observed. The shared cholesterol-medication item is a pragmatic public-data proxy and is tested in a measured-only sensitivity analysis.

Key secondary outcome:

- conventional metabolic syndrome, at least three of the four components above plus waist circumference at least 102 cm in men or 88 cm in women.

Exploratory outcomes:

- individual metabolic components;
- HbA1c;
- HOMA-IR after cycle-specific insulin verification;
- ALT and GGT;
- hs-CRP in 2015–2018 only.

## Covariates

The primary model includes age as a natural spline with three degrees of freedom, sex, race/ethnicity, survey cycle, education, poverty-income ratio, smoking status, and total fat-mass index. Covariates were selected for confounding control and design-period adjustment, not automated significance.

BMI and waist circumference are not included in the primary explanatory model. BMI replaces total fat-mass index in one sensitivity analysis. Waist is part of the conventional metabolic-syndrome outcome and is not used as an explanatory covariate for that outcome.

## Primary analysis

- survey-weighted generalized linear model;
- quasipoisson family with log link;
- design-robust variance;
- exposure, sex, and exposure-by-sex interaction;
- prevalence ratios and 95% confidence intervals;
- two-sided alpha 0.05 for the single primary interaction;
- sex-specific slopes derived from the pooled model;
- no claim of sex difference from separate within-sex significance tests.

A survey-weighted cubic polynomial exposure model assesses nonlinearity through joint tests of the quadratic and cubic terms and their sex interactions. This publication-stage implementation replaced an ambiguous spline-basis test without changing the frozen primary linear estimand. Secondary outcome families use Benjamini-Hochberg false-discovery control and are labelled exploratory.

## Missingness and sensitivity analyses

The primary analysis uses complete observations after separating planned fasting-subsample selection from item nonresponse. Sensitivities include:

- measured-only metabolic components;
- conventional metabolic syndrome;
- BMI rather than total fat-mass index;
- separate leg and trunk fat-mass indices;
- android-to-gynoid ratio;
- exclusion of 2017–2018;
- minimal covariate model;
- HOMA-IR and biomarker outcomes where harmonization is defensible.

No outcome-dependent imputation or model selection is permitted.

## Exploratory prediction analysis

Purpose: quantify whether regional DXA variables add temporally validated information beyond conventional measures.

Development cycles: 2011–2016. Protected temporal test cycle: 2017–2018.

Feature panels:

1. base demographics and socioeconomic variables;
2. base plus BMI;
3. base plus BMI and waist circumference;
4. base plus BMI, waist, total fat, leg-to-trunk ratio, android-to-gynoid ratio, and visceral fat.

Models:

- penalized logistic regression;
- spline logistic regression;
- XGBoost.

Models are tuned only in development data. Sample weights enter fitting and evaluation. Test metrics are weighted ROC AUC, average precision, log loss, Brier score, calibration intercept, and calibration slope. Panel 4 versus Panel 3 is the prespecified incremental comparison. No test-set-driven retuning is permitted.

As a publication-stage exploratory uncertainty analysis, 95% percentile intervals for ROC AUC and paired Panel 4 versus Panel 3 AUC differences are estimated from 1,000 bootstrap samples that resample primary sampling units with replacement within strata of the 2017–2018 holdout. This addition does not change model selection or the protected-test predictions.

Deep learning and neural networks are excluded because the sample is modest, inputs are tabular, raw DXA images are unavailable, and the added complexity is not justified.

## Stop and interpretation rules

- If interaction precision is poor, the interaction is reported as inconclusive and sex-specific estimates remain descriptive.
- If DXA does not improve temporal performance, the null incremental result is retained.
- Lipedema is not identified, classified, or assigned a prevalence.
- No “first”, causal, protective, clinical-utility, or diagnostic claim is permitted.
