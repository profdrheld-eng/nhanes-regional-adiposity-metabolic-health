# Methods draft

## Study design and population

We conducted a repeated cross-sectional analysis of the 2011–2018 National Health and Nutrition Examination Survey. The target population comprised noninstitutionalized US adults aged 20–59 years. Participants were eligible if they completed the mobile examination, were not pregnant, had a positive fasting-subsample weight, valid regional dual-energy X-ray absorptiometry measurements, all four primary metabolic components, and complete prespecified covariates.

## Exposure and outcomes

The primary exposure was the natural logarithm of leg fat mass divided by trunk fat mass. It was standardized using one pooled, fasting-weighted standard deviation. The primary outcome was metabolic dysfunction, defined as at least two of elevated triglycerides, reduced high-density lipoprotein cholesterol, elevated blood pressure, and elevated fasting glucose, with public questionnaire treatment indicators incorporated. Conventional metabolic syndrome was a secondary outcome.

## Statistical analysis

We used the fasting-subsample weights divided by four for pooled 2011–2018 inference and accounted for masked strata and primary sampling units. The primary survey-weighted quasipoisson model included the exposure, sex, their interaction, age as a natural spline, race and ethnicity, survey cycle, education, poverty-income ratio, smoking, and total fat-mass index. We report prevalence ratios with 95% confidence intervals. Sensitivity analyses tested measured-only components, conventional metabolic syndrome, alternative adiposity adjustment, component fat models, and cycle exclusion. Associations with the four individual metabolic components were exploratory, with Benjamini-Hochberg control of the false-discovery rate for their interaction tests.

An exploratory prediction analysis compared penalized logistic regression, spline logistic regression, and XGBoost. Models were developed and tuned using 2011–2016 data and evaluated in 2017–2018, then rerun after documented data corrections without test-driven changes to candidate models. We assessed weighted discrimination, overall accuracy, and calibration. Deep learning was excluded a priori. As a publication-stage exploratory uncertainty analysis, 95% percentile intervals for ROC AUC and paired AUC differences were obtained from 1,000 bootstrap samples that used the Rao-Wu n_h−1 rescaled PSU subbootstrap within strata, conditional on the fitted models of the temporal holdout.
