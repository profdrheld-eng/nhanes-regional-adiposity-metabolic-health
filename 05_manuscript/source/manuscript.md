# Leg-to-trunk fat distribution and metabolic dysfunction beyond total adiposity in US adults: a repeated cross-sectional NHANES 2011–2018 study

## Running title

Regional fat distribution and metabolic dysfunction

## Abstract

### Background

Regional fat distribution may distinguish metabolic heterogeneity beyond overall adiposity.

### Objective

We examined adiposity-adjusted leg-to-trunk fat–metabolic dysfunction associations, sex heterogeneity, and incremental discrimination from dual-energy X-ray absorptiometry (DXA).

### Methods

This repeated cross-sectional National Health and Nutrition Examination Survey (NHANES) 2011–2018 analysis included 3,971 adults aged 20–59 years. Metabolic dysfunction required at least two of four non-anthropometric components. Survey-weighted modified Poisson models adjusted for total fat-mass index estimated prevalence ratios (PRs). Exploratory contemporaneous prediction used 2011–2016 development and 2017–2018 testing (n = 751).

### Results

Per standard deviation higher log leg-to-trunk ratio, adjusted PRs were 0.71 (95% confidence interval [CI], 0.66 to 0.77) in male and 0.64 (95% CI, 0.60 to 0.69) in female participants. The log-linear interaction ratio was 0.90 (95% CI, 0.83 to 0.98; p = 0.014). Curvature was supported; overall sex heterogeneity in the cubic model was not (p = 0.683). Penalized logistic regression with total and regional DXA measures achieved a weighted area under the receiver operating characteristic curve of 0.811 (95% rescaled-bootstrap CI, 0.760 to 0.868); the increase beyond body mass index and waist was 0.033 (95% CI, 0.011 to 0.055). Intervals condition on trained models.

### Conclusions

Leg-predominant fat distribution was inversely associated with metabolic dysfunction after total-adiposity adjustment in both sexes under the log-linear model. Sex heterogeneity was model dependent. Total and regional DXA measures added modest discrimination; causality and clinical utility remain unestablished.

## Keywords

body composition; cardiometabolic health; dual-energy X-ray absorptiometry; lower-body adiposity; metabolic heterogeneity; sex differences

## 1 Introduction

Body mass index (BMI) remains the most widely used measure for classifying underweight, overweight, and obesity, and waist circumference adds information about abdominal adiposity (Nuttall, 2015; Ross et al., 2020). Neither measure, however, distinguishes fat from lean tissue or resolves anatomically and biologically distinct fat depots. This matters because metabolic complications vary substantially among people with similar BMI values, including people with normal weight or obesity (Jensen, 2008; Tchernof & Després, 2013; Anand et al., 2025). Waist circumference cannot separate abdominal subcutaneous from visceral fat and provides no direct information about lower-body storage. More detailed body-composition phenotyping may therefore clarify heterogeneity in dyslipidemia, blood pressure, glycemia, and insulin resistance.

Adipose tissue distribution is also functional (Jensen, 2008; Karastergiou et al., 2012; Tchernof & Després, 2013). Depots differ in adipocyte expandability, lipid turnover, endocrine activity, inflammatory signaling, and access to the portal circulation (Manolopoulos et al., 2010; Karastergiou et al., 2012; Tchernof & Després, 2013; Goossens et al., 2021). Visceral and ectopic fat is associated with insulin resistance and cardiometabolic morbidity, whereas gluteofemoral subcutaneous tissue may provide comparatively stable long-term lipid storage (Manolopoulos et al., 2010; Tchernof & Després, 2013; Neeland et al., 2019). Under the adipose-tissue expandability model, limited peripheral capacity may promote lipid spillover into non-adipose tissues (Virtue & Vidal-Puig, 2010). Human genetic evidence supports its plausibility: insulin-resistance-associated loci have been linked to lower peripheral adipose mass and impaired adipocyte differentiation despite BMI adjustment (Lotta et al., 2017). A larger lower-body compartment may thus mark greater peripheral storage capacity, although an observational ratio cannot establish this mechanism.

Population and imaging studies support opposing associations of central and lower-body fat with metabolic health (Grundy et al., 2008; Wu et al., 2010; Schorr et al., 2018; Yang et al., 2021). In the Dallas Heart Study, total fat and truncal-to-lower-body distribution contributed independently to several metabolic-syndrome components, with contributions differing across lipids, insulin resistance, blood pressure, and inflammation (Grundy et al., 2008). Other dual-energy X-ray absorptiometry (DXA) studies associated greater trunk, android, or visceral fat with less favorable profiles and greater leg or gluteofemoral fat, conditional on total or central adiposity, with more favorable metabolic profiles (Wu et al., 2010; Han et al., 2017; Schorr et al., 2018; Yang et al., 2021). Prospective anthropometric evidence is directionally consistent: abdominal measures were positively associated with coronary heart disease, whereas hip circumference adjusted for BMI and waist circumference was inversely associated in female and male participants (Canoy et al., 2007). Nevertheless, direct regional-fat studies are predominantly cross-sectional and use heterogeneous imaging regions, ratios, and outcomes (Wu et al., 2010; Schorr et al., 2018; Yang et al., 2021). They support regional adiposity as a marker of metabolic heterogeneity but do not establish that increasing leg fat would reduce risk (Canoy et al., 2007; Neeland et al., 2019).

Sex is central because female and male participants differ in total fat mass, depot preference, adipocyte biology, and hormonal regulation (Karastergiou et al., 2012; Gavin & Bessesen, 2020; Goossens et al., 2021). Female participants generally store more fat in gluteofemoral subcutaneous depots, whereas male participants tend to accumulate more trunk and visceral fat at a comparable BMI (Karastergiou et al., 2012; Hinton et al., 2017; Gavin & Bessesen, 2020; Goossens et al., 2021). Sex steroids, depot-specific adipogenesis and lipolysis, and sexually dimorphic genetic regulation may contribute (Lumish et al., 2020; Gavin & Bessesen, 2020). The metabolic evidence is not uniform. Schorr et al. (2018) reported a stronger favorable relation of lower-extremity fat among female participants, whereas Yang et al. (2021) found inverse associations in both sexes and larger estimates for some outcomes among male participants. Differences in age, menopause or hormone status, adiposity range, population composition, exposure scaling, and adjustment may contribute to this inconsistency (Schorr et al., 2018; Yang et al., 2021; Goossens et al., 2021). Sex-stratified estimates also do not establish statistical heterogeneity without a direct interaction test.

Recent National Health and Nutrition Examination Survey (NHANES) studies have refined the evidence by examining android and gynoid fat in metabolically healthy and unhealthy BMI groups and in relation to prediabetes (Anand et al., 2025; Shi et al., 2026). Together with earlier regional-fat studies, these findings establish the relevance of body-fat distribution but leave several connected questions incompletely resolved (Wu et al., 2010; Han et al., 2017; Anand et al., 2025; Shi et al., 2026). First, the association of a continuous leg-to-trunk fat phenotype with metabolic dysfunction should be separated from total adiposity rather than treated as a proxy for lower body weight. Second, conventional metabolic syndrome includes waist circumference; using a central-adiposity measure in both the exposure construct and the outcome can complicate interpretation of regional-fat associations (Alberti et al., 2009). Third, formal exposure-by-sex heterogeneity and the additional information conveyed by total and regional DXA measures beyond BMI and waist circumference address different but complementary questions. Evaluating both within one reproducible framework can distinguish adjusted cross-sectional association from incremental discrimination and show how these findings depend on exposure-model form and prediction-model complexity.

We therefore examined whether a greater leg-to-trunk fat-mass ratio was associated with a lower prevalence of non-anthropometric metabolic dysfunction in US adults aged 20 to 59 years after accounting for total fat-mass index and major demographic and behavioral covariates. Our prespecified primary hypothesis was that this inverse association would be stronger among female than male participants; we tested it using a direct exposure-by-sex interaction and assessed its dependence on exposure-model form. In a complementary exploratory analysis, we assessed whether total and regional DXA features added discriminatory information beyond demographics, BMI, and waist circumference in a temporal holdout, and whether spline-based or boosted models improved performance over penalized logistic regression. Together, these analyses assess regional adiposity as a marker of metabolic heterogeneity beyond overall adiposity and quantify the additional information in a combined DXA panel; they do not establish causality or clinical utility.

## 2 Methods

### Study Design

We conducted a repeated cross-sectional analysis of the 2011–2012, 2013–2014, 2015–2016, and 2017–2018 NHANES cycles. NHANES uses a stratified, clustered, multistage probability design to represent the noninstitutionalized civilian US population and releases public-use data in 2-year cycles (Chen et al., 2018; Chen et al., 2020). The National Center for Health Statistics Research Ethics Review Board approved the NHANES protocols, and participants provided written informed consent (National Center for Health Statistics, 2026). This secondary analysis used deidentified public data and involved no new participant contact. Reporting of the association analysis was guided by the Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement, and reporting of the exploratory prediction analysis was informed by the Transparent Reporting of a Multivariable Prediction Model for Individual Prognosis or Diagnosis plus Artificial Intelligence (TRIPOD+AI) recommendations (von Elm et al., 2007; Collins et al., 2024). The accompanying Supplementary File contains Supplementary Methods S1–S2, all Supplementary Tables S1–S11 (including lettered subtables), Figures S1–S3, and item-by-item reporting checklists with locations and remaining limitations.

### Study Population

We considered all participants in the four public 2-year survey cycles and applied the following sequential eligibility criteria; no sampling from eligible records was performed. Participants were eligible if they were examined in the mobile examination center, were aged 20 to 59 years, were not pregnant, and had a positive fasting-subsample weight. The upper age limit corresponded to the public whole-body DXA examination range. The primary analysis additionally required valid positive left-leg, right-leg, trunk, and total fat-mass measurements; classifiable values for all four metabolic components; and complete prespecified covariates.

No a priori sample-size calculation was performed because the analysis included all eligible observations from the fixed public survey cycles. Precision was assessed using design-based confidence intervals and survey degrees of freedom.

### Measurements and Outcomes

#### Body composition and primary exposure

NHANES measured whole-body composition by DXA using standardized examination procedures and centralized quality control (National Center for Health Statistics, 2020, 2021). We obtained left-leg fat mass, right-leg fat mass, trunk fat mass, total fat mass, android-to-gynoid ratio, and visceral adipose tissue mass from the public DXA files. Regional reference studies using earlier NHANES cycles demonstrate substantial sex and ethnicity differences in limb and trunk composition, supporting explicit adjustment and interaction assessment (Hinton et al., 2017).

The primary exposure was the natural logarithm of the ratio of total leg fat mass to trunk fat mass: `log[(left-leg fat mass + right-leg fat mass) / trunk fat mass]`. Higher values indicated more leg fat relative to trunk fat. Alternative regional measures were leg fat-mass index, trunk fat-mass index, android-to-gynoid ratio, and visceral adipose tissue mass.

#### Metabolic outcomes

The primary outcome was non-anthropometric metabolic dysfunction, defined as at least two of four components:

1. triglycerides of at least 150 mg/dL or a positive public cholesterol-treatment indicator;
2. high-density lipoprotein cholesterol below 40 mg/dL in male participants or below 50 mg/dL in female participants, or a positive public cholesterol-treatment indicator;
3. mean systolic blood pressure of at least 130 mmHg, mean diastolic blood pressure of at least 85 mmHg, or reported antihypertensive treatment;
4. fasting plasma glucose of at least 100 mg/dL, diagnosed diabetes, insulin treatment, or oral diabetes medication.

All four components had to be classifiable. An unequivocal positive measured or treatment finding classified a component as positive even if another input was unknown; a negative component required all inputs to be known negative. Blood-pressure values were averaged across available valid readings. The shared cholesterol-treatment item was treated as a pragmatic proxy because public NHANES files do not identify lipid-lowering indication with full clinical specificity. A conservative sensitivity outcome allowed the generic lipid-treatment indicator to represent at most one dyslipidemia component and did not let it add a second component when either measured lipid abnormality was already present.

The key secondary outcome was conventional metabolic syndrome, defined as any three of five components: the four components above and waist circumference of at least 102 cm in male participants or 88 cm in female participants (Alberti et al., 2009). A further measured-only sensitivity outcome ignored medication indicators. The four individual metabolic components were evaluated exploratorily.

#### Covariates

The primary model adjusted for age, sex, ethnicity, survey cycle, educational attainment, family income relative to the federal poverty threshold, smoking status, and total fat-mass index. Age was modeled flexibly using a spline with three degrees of freedom, and ethnicity was based on the standard categories provided by NHANES. We selected all covariates before the analysis to account for demographic, socioeconomic, behavioral, survey-period, and overall-adiposity differences. BMI was examined as an alternative measure of overall adiposity in a sensitivity analysis. Waist circumference was not included in the primary model, which assessed the regional-fat association conditional on overall adiposity rather than on an additional central-adiposity measure. NHANES records sex only as male or female.

### Data Preparation

Public examination, laboratory, questionnaire, and DXA files were harmonized across survey cycles and linked using the unique participant identifier. Cycle-specific variable names and coding schemes were standardized before variables were derived. Blood-pressure values were averaged across all available valid readings. The four metabolic components were then constructed from measured values and the public treatment indicators. BPQ040A and BPQ090D identified structurally negative medication skips in all four cycles. Direct current-use responses took precedence; a negative recommendation response implied no treatment, whereas refusal or unknown responses were not coded as no treatment. The variable-level rules, coding and missingness are provided in Supplementary Methods S1 and Tables S3–S5.

The primary exposure was calculated after excluding nonpositive regional fat-mass values and was standardized once using the fasting-weighted mean and standard deviation of the primary analysis population. Total, leg, and trunk fat-mass indices were calculated as the corresponding fat mass in kilograms divided by height in meters squared. We divided the 2-year fasting-subsample weight by four to obtain pooled 2011–2018 weights in accordance with NHANES guidance for combining equally long survey cycles (Chen et al., 2018; Chen et al., 2020; National Center for Health Statistics, 2018). The complex survey design was constructed before the complete-case analysis domain was defined so that subpopulation variance estimation retained the full design information.

The primary association analysis used complete observations, and outcomes were not imputed. For the prediction analysis, preprocessing was estimated within each development fold. Numerical predictors were imputed with the development-fold median and standardized. Categorical predictors were imputed with the development-fold mode and one-hot encoded. No preprocessing parameter was estimated from the temporal holdout. Unseen categorical levels, including the held-out cycle, were encoded as all-zero indicators. Imputation of additional prediction features occurred within the already selected primary complete-case sample.

### Statistical Analysis

#### Survey-weighted association analysis

Analyses incorporated pooled fasting-subsample weights, masked strata, and primary sampling units and used an adjustment for lonely primary sampling units (Chen et al., 2018; Chen et al., 2020; Lumley, 2004). Continuous descriptive variables are reported as weighted arithmetic means with weighted standard deviations. Categorical characteristics are reported as weighted percentages; unweighted counts are additionally provided for the total sample and metabolic dysfunction. We estimated prevalence ratios (PRs) using survey-weighted generalized linear models with a log link, quasipoisson variance, and design-robust standard errors. Modified Poisson modeling provides direct ratio estimates for common binary outcomes when combined with robust variance estimation (Zou, 2004).

The primary model included the standardized log leg-to-trunk ratio, sex, and their interaction. Sex-specific exposure estimates and the female-to-male ratio of PRs were derived as linear contrasts from the same pooled model. All tests were two-sided, and 95% Wald confidence intervals (CIs) and p values from survey generalized linear models used a t reference distribution with the model residual design degrees of freedom. The prespecified exposure-by-sex interaction was the single primary hypothesis and was evaluated at alpha = 0.05. We did not infer sex differences from separate within-sex p values.

A secondary polynomial model added quadratic and cubic exposure terms and their interactions with sex. A four-degree-of-freedom joint design-based Wald F test assessed quadratic and cubic curvature across sexes. Two-degree-of-freedom tests separately assessed curvature in the male reference group and additional curvature-by-sex interaction. A revision-stage three-degree-of-freedom test assessed all exposure-by-sex terms together. We added unadjusted sex-specific estimates for reporting completeness, plotted the existing cubic model with exposure support, and counted fitted means above one. These additions were fixed before the corrected rerun and were not independently preregistered. All tests reported numerator and denominator degrees of freedom. Sensitivity analyses used the conservative single-count lipid-medication outcome, the measured-only outcome, conventional metabolic syndrome, BMI instead of total fat-mass index, a minimally adjusted model, exclusion of 2017–2018, android-to-gynoid ratio, visceral adipose tissue, and simultaneous leg and trunk fat-mass indices. These analyses were interpreted as secondary rather than as independent confirmations of the primary hypothesis. The four individual-component interactions were exploratory, and their p values were adjusted as one family using the Benjamini-Hochberg false-discovery-rate procedure (Benjamini & Hochberg, 1995).

Prespecified exploratory biomarker analyses were not included in the final manuscript because their cycle coverage and analysis populations differed from the primary analysis. They were not used to select or interpret the primary result.

#### Exploratory temporal-holdout prediction analysis

The prediction analysis assessed whether total and regional DXA features jointly added discriminatory information beyond conventional measures. Its target was metabolic dysfunction measured at the same examination as the predictors; the temporal split assessed transportability across survey cycles, not prospective risk prediction. The same 3,971 participants included in the primary analysis were temporally divided into a development sample of 3,220 participants from 2011–2016 and a holdout sample of 751 participants from 2017–2018. Development-only cross-validation selected hyperparameters from the original fixed grids. The holdout had already been inspected in an earlier draft; the present revision corrected data coding and uncertainty estimation without changing panels, model families, grids or the temporal split in response to test performance.

Four nested feature panels were compared:

1. age, sex, ethnicity, cycle, education, poverty-income ratio, and smoking;
2. panel 1 plus BMI;
3. panel 2 plus waist circumference;
4. panel 3 plus total fat-mass index, log leg-to-trunk ratio, android-to-gynoid ratio, and visceral adipose tissue mass.

We compared L2-penalized logistic regression, logistic regression with spline-transformed continuous predictors, and XGBoost (Chen & Guestrin, 2016). Candidate hyperparameters were fixed before holdout evaluation. For both logistic models, the inverse regularization strength was 0.1, 1.0, or 10.0; spline models used five knots and cubic basis functions. The three XGBoost candidates combined maximum depths of 2 or 3, learning rates of 0.03 or 0.05, and 180 or 250 trees, with the remaining regularization and sampling settings held fixed. Hyperparameters were selected in the development sample using leave-one-cycle-out grouped cross-validation and weighted log loss. Survey weights were normalized to a mean of one for model fitting and retained on their original relative scale for evaluation.

Holdout performance measures were the weighted area under the receiver operating characteristic curve (ROC AUC), weighted average precision, log loss, Brier score, calibration intercept, and calibration slope, thereby covering discrimination, overall predictive accuracy, and calibration (Steyerberg & Vergouwe, 2014; Collins et al., 2024). The prespecified incremental comparison was panel 4 versus panel 3. As a revision-stage exploratory uncertainty analysis, we generated 1,000 Rao-Wu rescaled subbootstrap replicates. Within each holdout stratum containing n_h primary sampling units (PSUs), n_h−1 PSUs were drawn with replacement and multiplicities were multiplied by n_h/(n_h−1). All 15 strata contained two PSUs. The same replicate weights were used across all models. Percentile intervals were calculated for ROC AUC, paired AUC differences, and calibration parameters. These intervals condition on the fitted models and do not capture development or tuning uncertainty. Calibration intercept and slope were estimated jointly by weighted logistic regression of outcome on the predicted logit; the intercept is not calibration-in-the-large with slope fixed to one. Supplementary Figure S2 presents descriptive calibration bins. Because model-class and feature-panel comparisons were exploratory, these intervals were treated as descriptive uncertainty estimates rather than confirmatory hypothesis tests, and no multiplicity-adjusted prediction claims were made. Deep neural networks were not evaluated because the development sample was modest for such models, the predictors were low-dimensional tabular variables, and empirical work indicates substantially larger samples are often required for stable neural-network performance than for logistic regression (Silvey & Liu, 2024).

#### Software and reproducibility

Data harmonization and survey analyses used R 4.6.0, the survey package 4.5, and splines 4.6.0 (Lumley, 2004). Prediction analyses used Python 3.9.6, pandas 2.3.3, NumPy 2.0.2, scikit-learn 1.6.1, XGBoost 2.1.4, and statsmodels 0.14.6. The random seed was 20260726. The original local analysis plan and configuration were retained, with a dated revision amendment documenting corrected questionnaire skips, three-valued outcome logic, rescaled bootstrap intervals and expanded reporting. Local freezing is not evidence of independent preregistration. Source files were checked against a frozen manifest using file size and MD5 hashes. The full pipeline generated a SHA-256 artifact manifest and failed closed when required outputs, estimates, probabilities, or source files were missing or invalid.

## 3 Results

### Participant flow and characteristics

Across 2011–2018, 14,100 examined participants met the age and pregnancy criteria; 6,050 had positive fasting weights, 4,415 had valid required DXA measures, 4,299 had all four metabolic components classifiable, and 3,971 had complete primary covariates. The final sample comprised 2,008 male and 1,963 female participants. The survey design contributed 62 degrees of freedom; the fully adjusted primary model had 40 residual design degrees of freedom. Supplementary Figure S3 shows participant flow and sequential exclusions; Supplementary Tables S3–S5 report cycle-specific counts, preselection missingness and medication-skip checks.

Metabolic dysfunction was present in 1,643 participants. Weighted age, adiposity, socioeconomic characteristics and outcome prevalence by sex are reported in Table 1. Correcting the questionnaire skips and component logic added 667 participants to the earlier analysis; no previously included participant was removed. This correction addresses avoidable exclusions but does not eliminate selection from genuine missingness.

### Primary association

After adjustment for total fat-mass index and the prespecified covariates, per 1-standard-deviation higher log leg-to-trunk fat-mass ratio, PRs were 0.71 (95% CI, 0.66 to 0.77; p < 0.001) in male participants and 0.64 (95% CI, 0.60 to 0.69; p < 0.001) in female participants. The female-to-male ratio of PRs was 0.90 (95% CI, 0.83 to 0.98; p = 0.014). This contrast describes the imposed log-linear exposure relation (Figures 1 and 2).

The cubic model supported curvature across sexes (F(4, 36) = 8.63, p < 0.001). Neither the additional curvature-by-sex terms (F(2, 36) = 0.73, p = 0.490) nor all exposure-by-sex terms jointly (F(3, 36) = 0.50, p = 0.683) supported a sex difference in the flexible model. The primary and cubic models produced 158 and 130 fitted means above one, respectively (maxima 2.95 and 3.03). Both converged. These diagnostics limit probability interpretation and support treating the linear sex contrast as model dependent. Flexible curves, pointwise uncertainty, exposure support and diagnostics are shown in Supplementary Figure S1 and Table S7.

### Sensitivity and exploratory association analyses

The single-count lipid-medication interaction ratio was 0.92 (95% CI, 0.85 to 1.00; p = 0.062); the measured-only ratio was 0.85 (95% CI, 0.77 to 0.93; p < 0.001). The corresponding ratios were 0.90 (95% CI, 0.83 to 0.98; p = 0.014) after BMI adjustment, 0.93 (95% CI, 0.84 to 1.02; p = 0.123) after excluding 2017–2018, and 1.09 (95% CI, 0.99 to 1.20; p = 0.093) for the five-component metabolic-syndrome outcome. Sensitivity populations differed where their outcome inputs were missing. Table 2 and Supplementary Table S6 report all variants, including both sex-specific estimates, sample sizes and cases.

In the joint leg-and-trunk model, the male-reference PRs were 0.76 (95% CI, 0.66 to 0.88; p < 0.001) for leg fat-mass index and 1.74 (95% CI, 1.55 to 1.96; p < 0.001) for trunk fat-mass index. Sex-specific contrasts and interactions for both depots and the alternative regional measures are given in Supplementary Table S6. These conditional associations do not identify an effect of changing either depot.

All four exploratory component interactions, including their Benjamini-Hochberg-adjusted p values, are reported in Supplementary Table S1. Components incorporate treatment indicators and should not be interpreted as measured biomarker concentrations alone.

### Temporal-holdout prediction

Development included 3,220 participants (1,314 cases) and temporal testing included 751 participants (329 cases). Supplementary Table S8 compares these samples, including predictor missingness. Figure 3 shows all four panels and three model classes.

For penalized logistic regression, the full DXA panel had a weighted ROC AUC of 0.811 (95% cluster-bootstrap CI, 0.760 to 0.868), average precision 0.720, log loss 0.514, Brier score 0.170, joint calibration intercept -0.031, and slope 0.956 (Table 3). Adding total and regional DXA features jointly increased AUC by 0.033 (95% paired cluster-bootstrap CI, 0.011 to 0.055). Here and throughout, cluster-bootstrap intervals use the rescaled procedure described in Methods.

The AUC increment was 0.036 (95% CI, 0.013 to 0.057) for spline logistic regression and 0.031 (95% CI, 0.012 to 0.050) for XGBoost. Penalized logistic regression had the lowest observed full-panel log loss; spline logistic regression had a slightly higher observed AUC. These descriptive differences do not establish equivalence or model-class superiority. Supplementary Tables S2 and S9–S11 provide paired increments, development tuning, selected settings and calibration intervals; Supplementary Figure S2 shows calibration plots.

## 4 Discussion

In this survey-weighted repeated cross-sectional sample of US adults aged 20 to 59 years, a more leg-predominant fat distribution was associated with a lower prevalence of non-anthropometric metabolic dysfunction after accounting for total fat-mass index and major demographic and behavioral covariates. The log-linear association was inverse in both sexes. These adjusted associations support regional fat distribution as a marker of metabolic heterogeneity beyond overall adiposity. The prespecified hypothesis of a stronger association in female participants was not consistently supported across exposure models and outcome definitions. Total and regional DXA measures jointly added modest discriminatory information beyond BMI and waist circumference in an exploratory temporal holdout.

The direction of our regional-fat findings was consistent with previous studies, although the magnitude and sex-specific pattern were heterogeneous. Wu et al. (2010) reported inverse associations of leg fat and adverse associations of trunk fat with metabolic syndrome and related biomarkers in both sexes. Han et al. (2017) similarly associated a higher leg-to-total-fat ratio with lower estimated cardiovascular risk, although that study did not test the same leg-to-trunk-by-sex interaction. Schorr et al. (2018) reported a stronger favorable association of lower-extremity fat among female participants, whereas Yang et al. (2021) observed inverse lower-body associations in both sexes but larger estimates for clustered cardiometabolic risk among male participants. Our joint leg-and-trunk fat-mass model likewise showed an inverse association for leg fat and a positive association for trunk fat; the full sex-specific contrasts are reported to distinguish reference-group coefficients from population-wide statements.

The log-linear sex contrast depends on the exposure model and outcome definition, which limits biological interpretation. Female participants generally have greater gluteofemoral storage capacity, and sex steroids, adipocyte precursor properties, lipid turnover, and depot-specific adipokine secretion may contribute to different regional responses (Karastergiou et al., 2012; Goossens et al., 2021). However, the heterogeneous sex patterns across previous studies mean that our interaction should not be interpreted as an established universal difference. It may reflect sex-related biology, unmeasured menopause or hormone status, differences in the distribution and range of the ratio, or residual confounding. NHANES cannot distinguish these explanations.

Recent NHANES studies make careful positioning essential. Anand et al. (2025) used the same 2011–2018 cycles and a closely related 2-of-4 metabolic outcome, finding different android and gynoid patterns across metabolically healthy and unhealthy BMI groups. Shi et al. (2026) reported sex-specific associations of android and gynoid adiposity with prediabetes in NHANES 2011–2016. The present study extends rather than replaces this evidence by using a continuous leg-to-trunk phenotype, directly estimating a sex interaction while adjusting for total fat-mass index, and quantifying the incremental information in total and regional DXA features jointly in a temporally separated survey cycle. The overlap with these publications precludes a broad novelty claim.

The prediction results provide a complementary methodological finding. Total and regional DXA features jointly improved temporal-holdout discrimination beyond BMI and waist circumference across all three model classes, and the paired bootstrap intervals excluded zero. However, the absolute improvement was modest, the holdout contained only 751 participants, and a temporal split within NHANES is not an external validation in a different population or clinical setting. Because predictors and outcome were measured contemporaneously, this analysis evaluated discrimination of current metabolic status rather than future risk. Penalized logistic regression had the lowest observed log loss, while spline logistic regression had a slightly higher observed AUC. The corrected intervals condition on trained models and do not include development uncertainty. This agrees with empirical evidence that complex models may need substantially larger samples to stabilize in tabular clinical data and that model complexity does not guarantee better performance (Silvey & Liu, 2024). Because the added panel included total fat-mass index, the AUC increment cannot be attributed to regional fat distribution alone. These results support further evaluation of the combined DXA panel but do not establish a benefit from routine DXA screening.

Several mechanisms could underlie the observed associations. Gluteofemoral adipose tissue has lower lipid turnover than abdominal depots and may provide longer-term storage of excess fatty acids, potentially limiting ectopic lipid exposure. Lower-body fat has also been associated with higher adiponectin and a less inflammatory profile, while trunk and visceral depots are more strongly linked with insulin resistance and adverse lipid metabolism (Manolopoulos et al., 2010; Wu et al., 2010; Karastergiou et al., 2012). These mechanisms are consistent with the observed opposite leg and trunk associations and the exploratory glucose interaction. Nevertheless, the present data contain no direct depot-specific flux, tissue biology, or prospective disease measurements. Mechanistic explanations remain hypotheses.

The study has several limitations. First, NHANES is cross-sectional, so temporality and causality cannot be established. Because exposure and outcome were measured at the same examination, temporal ordering is unknown and reverse association cannot be excluded. Second, the primary outcome is a pragmatic research construct rather than a clinical diagnosis. The public cholesterol-treatment item may not perfectly identify treatment for elevated triglycerides or reduced high-density lipoprotein cholesterol. Because the same generic item was applied to both lipid components, it could contribute twice to the primary component count. The alternative outcome definitions did not eliminate misclassification and gave different interaction estimates. Uniform waist thresholds in the secondary five-component outcome also limit clinical comparability across ethnic groups. Third, complete-case selection reduced 4,415 participants with valid DXA data to 3,971 in the primary model. Survey weighting addresses the sampling design but does not guarantee correction of selection related to missing analysis variables. Fourth, residual confounding may remain, particularly from physical activity, diet, menopause, sex hormones, medication type, and prior weight change. Fifth, the binary public sex variable does not capture gender identity or hormonal status. Sixth, the DXA age restriction limits inference to adults aged 20 to 59 years. Scanner restrictions and incomplete DXA measurements may further select participants by body size; standard sampling weights do not necessarily correct this analysis-specific selection. Seventh, the modified Poisson models produced fitted means above one, limiting their interpretation as individual probabilities; the supported curvature also limits a constant log-linear PR across the exposure range. Eighth, the exploratory component analyses and bootstrap uncertainty analysis were secondary, and the temporal-holdout sample was modest. Finally, the same NHANES cycles have been used in recent related publications, which limits novelty and makes independent replication particularly important (Anand et al., 2025; Shi et al., 2026).

Strengths include the nationally representative sampling frame, standardized DXA and laboratory measurements, explicit use of fasting-subsample weights and complex-survey variance estimation, a formal pooled interaction model, avoidance of waist circumference in the primary metabolic outcome, multiple exposure and outcome sensitivity analyses, a temporal holdout with no test-cycle retuning, and an executable local pipeline with source-file and artifact checks. Independent reproduction by researchers outside the author team remains pending.

These findings may help refine hypotheses for prospective and clinical studies of regional adipose biology. Future work should independently assess the regional-fat association and potential sex heterogeneity, evaluate menopause and hormone status, characterize adipose-tissue function directly, and test whether total and regional DXA measures improve decisions or outcomes beyond simpler anthropometry. Clinical studies of disorders with disproportionate lower-body adiposity require confirmed diagnoses and cannot be replaced by a population DXA ratio.

## Conclusion

A greater leg-to-trunk fat-mass ratio was associated with lower metabolic dysfunction prevalence after adjustment for total fat-mass index in the log-linear models for both sexes. These findings support regional fat distribution as a marker of metabolic heterogeneity beyond overall adiposity. A consistently stronger association in female participants was not established. Total and regional DXA features jointly added modest temporal-holdout discrimination beyond BMI and waist circumference. These findings do not establish causality, diagnostic utility, or clinical benefit.

## Data availability

NHANES data are publicly available from the US Centers for Disease Control and Prevention at https://www.cdc.gov/nchs/nhanes/. The analysis uses only deidentified public files.

## Code availability

The analysis code, frozen configuration, source manifest, aggregate reference results, and reproduction instructions are available at https://github.com/profdrheld-eng/nhanes-regional-adiposity-metabolic-health (release v1.0.0). The release is identified by its Git tag and commit hash; no separate code DOI is assigned. Participant-level data, predictions, and fitted model objects are generated locally and are not distributed in the repository.

## Ethics statement

NHANES protocols were approved by the National Center for Health Statistics Research Ethics Review Board, and participants provided written informed consent (National Center for Health Statistics, 2026). The Ethics Committee of IST Hochschule für Management und Sport, Düsseldorf, Germany, confirmed that a separate ethics opinion was not required for this secondary analysis of deidentified public data. There was no patient involvement in this secondary analysis.

## Funding

No specific funding was received for this work.

## Conflicts of interest

The authors declare no conflicts of interest.

## Author contributions

Steffen Held: Conceptualization, Formal analysis, Software, Writing – original draft, Writing – review & editing. Florian Micke: Writing – review & editing. Manuel Matzka: Writing – review & editing. Eduard Isenmann: Conceptualization, Writing – original draft, Writing – review & editing. All authors critically evaluated and revised the manuscript.

## Acknowledgments

We thank the National Center for Health Statistics and the NHANES team for making the survey data publicly available, and all NHANES participants for their contributions to the original survey.

## References

Alberti, K. G. M. M., Eckel, R. H., Grundy, S. M., Zimmet, P. Z., Cleeman, J. I., Donato, K. A., Fruchart, J.-C., James, W. P. T., Loria, C. M., & Smith, S. C., Jr. (2009). Harmonizing the metabolic syndrome: A joint interim statement. *Circulation, 120*(16), 1640–1645. https://doi.org/10.1161/CIRCULATIONAHA.109.192644 (PMID: 19805654)

Anand, S., Pasupneti, T., Pak, Y., Kalangi, S. T., & Garg, R. (2025). Differences in fat distribution between metabolically unhealthy people with normal weight versus obesity, NHANES 2011–2018. *BMJ Open Diabetes Research & Care, 13*(3), e005118. https://doi.org/10.1136/bmjdrc-2025-005118 (PMID: 40441740)

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society: Series B (Methodological), 57*(1), 289–300. https://doi.org/10.1111/j.2517-6161.1995.tb02031.x

Canoy, D., Boekholdt, S. M., Wareham, N., Luben, R., Welch, A., Bingham, S., Buchan, I., Day, N., & Khaw, K.-T. (2007). Body fat distribution and risk of coronary heart disease in men and women in the European Prospective Investigation Into Cancer and Nutrition in Norfolk cohort: A population-based prospective study. *Circulation, 116*(25), 2933–2943. https://doi.org/10.1161/CIRCULATIONAHA.106.673756 (PMID: 18071080)

Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 785–794). https://doi.org/10.1145/2939672.2939785

Chen, T.-C., Parker, J. D., Clark, J., Shin, H.-C., Rammon, J. R., & Burt, V. L. (2018). National Health and Nutrition Examination Survey: Estimation procedures, 2011–2014. *Vital and Health Statistics, Series 2*(177), 1–26. https://stacks.cdc.gov/view/cdc/51180

Chen, T.-C., Clark, J., Riddles, M. K., Mohadjer, L. K., & Fakhouri, T. H. I. (2020). National Health and Nutrition Examination Survey, 2015–2018: Sample design and estimation procedures. *Vital and Health Statistics, Series 2*(184), 1–35. https://www.cdc.gov/nchs/data/series/sr_02/sr02-184-508.pdf

Collins, G. S., Moons, K. G. M., Dhiman, P., Riley, R. D., Beam, A. L., Van Calster, B., Ghassemi, M., Liu, X., Reitsma, J. B., van Smeden, M., Boulesteix, A.-L., Camaradou, J. C., Celi, L. A., Denaxas, S., Denniston, A. K., Glocker, B., Golub, R. M., Harvey, H., Heinze, G., … Logullo, P. (2024). TRIPOD+AI statement: Updated guidance for reporting clinical prediction models that use regression or machine learning methods. *BMJ, 385*, e078378. https://doi.org/10.1136/bmj-2023-078378 (PMID: 38626948)

Gavin, K. M., & Bessesen, D. H. (2020). Sex differences in adipose tissue function. *Endocrinology and Metabolism Clinics of North America, 49*(2), 215–228. https://doi.org/10.1016/j.ecl.2020.02.008 (PMID: 32418585)

Goossens, G. H., Jocken, J. W. E., & Blaak, E. E. (2021). Sexual dimorphism in cardiometabolic health: The role of adipose tissue, muscle and liver. *Nature Reviews Endocrinology, 17*(1), 47–66. https://doi.org/10.1038/s41574-020-00431-8 (PMID: 33173188)

Grundy, S. M., Adams-Huet, B., & Vega, G. L. (2008). Variable contributions of fat content and distribution to metabolic syndrome risk factors. *Metabolic Syndrome and Related Disorders, 6*(4), 281–288. https://doi.org/10.1089/met.2008.0026 (PMID: 18759660)

Han, E., Lee, Y. H., Lee, B. W., Kang, E. S., Lee, I. K., & Cha, B. S. (2017). Anatomic fat depots and cardiovascular risk: A focus on the leg fat using nationwide surveys (KNHANES 2008–2011). *Cardiovascular Diabetology, 16*(1), 54. https://doi.org/10.1186/s12933-017-0536-4 (PMID: 28441953)

Hinton, B. J., Fan, B., Ng, B. K., & Shepherd, J. A. (2017). Dual energy X-ray absorptiometry body composition reference values of limbs and trunk from NHANES 1999–2004 with additional visualization methods. *PLOS ONE, 12*(3), e0174180. https://doi.org/10.1371/journal.pone.0174180 (PMID: 28346492)

Jensen, M. D. (2008). Role of body fat distribution and the metabolic complications of obesity. *The Journal of Clinical Endocrinology & Metabolism, 93*(11 Suppl 1), S57–S63. https://doi.org/10.1210/jc.2008-1585 (PMID: 18987271)

Karastergiou, K., Smith, S. R., Greenberg, A. S., & Fried, S. K. (2012). Sex differences in human adipose tissues: The biology of pear shape. *Biology of Sex Differences, 3*(1), 13. https://doi.org/10.1186/2042-6410-3-13 (PMID: 22651247)

Lotta, L. A., Gulati, P., Day, F. R., Payne, F., Ongen, H., van de Bunt, M., Gaulton, K. J., Eicher, J. D., Sharp, S. J., Luan, J., De Lucia Rolfe, E., Stewart, I. D., Wheeler, E., Willems, S. M., Adams, C., Yaghootkar, H., Forouhi, N. G., Khaw, K.-T., Johnson, A. D., … Scott, R. A. (2017). Integrative genomic analysis implicates limited peripheral adipose storage capacity in the pathogenesis of human insulin resistance. *Nature Genetics, 49*(1), 17–26. https://doi.org/10.1038/ng.3714 (PMID: 27841877)

Lumish, H. S., O'Reilly, M., & Reilly, M. P. (2020). Sex differences in genomic drivers of adipose distribution and related cardiometabolic disorders: Opportunities for precision medicine. *Arteriosclerosis, Thrombosis, and Vascular Biology, 40*(1), 45–60. https://doi.org/10.1161/ATVBAHA.119.313154 (PMID: 31747800)

Lumley, T. (2004). Analysis of complex survey samples. *Journal of Statistical Software, 9*(8), 1–19. https://doi.org/10.18637/jss.v009.i08

Manolopoulos, K. N., Karpe, F., & Frayn, K. N. (2010). Gluteofemoral body fat as a determinant of metabolic health. *International Journal of Obesity, 34*(6), 949–959. https://doi.org/10.1038/ijo.2009.286 (PMID: 20065965)

National Center for Health Statistics. (2018). *National Health and Nutrition Examination Survey: Analytic guidelines, 2011–2016*. Centers for Disease Control and Prevention. https://wwwn.cdc.gov/nchs/data/nhanes/analyticguidelines/11-16-analytic-guidelines.pdf

National Center for Health Statistics. (2020). *2017–2018 data documentation, codebook, and frequencies: Dual-energy X-ray absorptiometry, whole body (DXX_J)*. Centers for Disease Control and Prevention. https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/DXX_J.htm

National Center for Health Statistics. (2021). *2017–2018 data documentation, codebook, and frequencies: Dual-energy X-ray absorptiometry, android/gynoid measurements (DXXAG_J)*. Centers for Disease Control and Prevention. https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/DXXAG_J.htm

National Center for Health Statistics. (2026). *NCHS Research Ethics Review Board approval*. Centers for Disease Control and Prevention. https://www.cdc.gov/nchs/nhanes/about/erb.html

Neeland, I. J., Ross, R., Després, J.-P., Matsuzawa, Y., Yamashita, S., Shai, I., Seidell, J., Magni, P., Santos, R. D., Arsenault, B., Cuevas, A., Hu, F. B., Griffin, B., Zambon, A., Barter, P., Fruchart, J.-C., & Eckel, R. H. (2019). Visceral and ectopic fat, atherosclerosis, and cardiometabolic disease: A position statement. *The Lancet Diabetes & Endocrinology, 7*(9), 715–725. https://doi.org/10.1016/S2213-8587(19)30084-1 (PMID: 31301983)

Nuttall, F. Q. (2015). Body mass index: Obesity, BMI, and health: A critical review. *Nutrition Today, 50*(3), 117–128. https://doi.org/10.1097/NT.0000000000000092 (PMID: 27340299)

Ross, R., Neeland, I. J., Yamashita, S., Shai, I., Seidell, J., Magni, P., Santos, R. D., Arsenault, B., Cuevas, A., Hu, F. B., Griffin, B. A., Zambon, A., Barter, P., Fruchart, J.-C., Eckel, R. H., Matsuzawa, Y., & Després, J.-P. (2020). Waist circumference as a vital sign in clinical practice: A consensus statement from the IAS and ICCR Working Group on Visceral Obesity. *Nature Reviews Endocrinology, 16*(3), 177–189. https://doi.org/10.1038/s41574-019-0310-7 (PMID: 32020062)

Schorr, M., Dichtel, L. E., Gerweck, A. V., Valera, R. D., Torriani, M., Miller, K. K., & Bredella, M. A. (2018). Sex differences in body composition and association with cardiometabolic risk. *Biology of Sex Differences, 9*(1), 28. https://doi.org/10.1186/s13293-018-0189-3 (PMID: 29950175)

Shi, Z., Xu, Q., Yin, R., Zhou, Q., & Wu, C. (2026). Sex-specific associations of android and gynoid adiposity with prediabetes among U.S. adults: A cross-sectional analysis of National Health and Nutrition Examination Survey 2011–2016. *Metabolic Syndrome and Related Disorders, 24*(7), 326–334. https://doi.org/10.1177/15578518261446293 (PMID: 42047492)

Silvey, S., & Liu, J. (2024). Sample size requirements for popular classification algorithms in tabular clinical data: Empirical study. *Journal of Medical Internet Research, 26*, e60231. https://doi.org/10.2196/60231 (PMID: 39689306)

Steyerberg, E. W., & Vergouwe, Y. (2014). Towards better clinical prediction models: Seven steps for development and an ABCD for validation. *European Heart Journal, 35*(29), 1925–1931. https://doi.org/10.1093/eurheartj/ehu207 (PMID: 24898551)

Tchernof, A., & Després, J.-P. (2013). Pathophysiology of human visceral obesity: An update. *Physiological Reviews, 93*(1), 359–404. https://doi.org/10.1152/physrev.00033.2011 (PMID: 23303913)

Virtue, S., & Vidal-Puig, A. (2010). Adipose tissue expandability, lipotoxicity and the metabolic syndrome: An allostatic perspective. *Biochimica et Biophysica Acta, 1801*(3), 338–349. https://doi.org/10.1016/j.bbalip.2009.12.006 (PMID: 20056169)

von Elm, E., Altman, D. G., Egger, M., Pocock, S. J., Gøtzsche, P. C., & Vandenbroucke, J. P. (2007). The Strengthening the Reporting of Observational Studies in Epidemiology statement: Guidelines for reporting observational studies. *The Lancet, 370*(9596), 1453–1457. https://doi.org/10.1016/S0140-6736(07)61602-X (PMID: 18064739)

Wu, H., Qi, Q., Yu, Z., Sun, Q., Wang, J., Franco, O. H., Sun, L., Li, H., Liu, Y., Hu, F. B., & Lin, X. (2010). Independent and opposite associations of trunk and leg fat depots with adipokines, inflammatory markers, and metabolic syndrome in middle-aged and older Chinese men and women. *The Journal of Clinical Endocrinology & Metabolism, 95*(9), 4389–4398. https://doi.org/10.1210/jc.2010-0181 (PMID: 20519350)

Yang, Y., Xie, M., Yuan, S., Zeng, Y., Dong, Y., Wang, Z., Xiao, Q., Dong, B., Ma, J., & Hu, J. (2021). Sex differences in the associations between adiposity distribution and cardiometabolic risk factors in overweight or obese individuals: A cross-sectional study. *BMC Public Health, 21*(1), 1232. https://doi.org/10.1186/s12889-021-11316-4 (PMID: 34174845)

Zou, G. (2004). A modified Poisson regression approach to prospective studies with binary data. *American Journal of Epidemiology, 159*(7), 702–706. https://doi.org/10.1093/aje/kwh090 (PMID: 15033648)
