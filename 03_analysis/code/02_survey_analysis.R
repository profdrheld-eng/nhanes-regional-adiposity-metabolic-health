#!/usr/bin/env Rscript

if (!requireNamespace("survey", quietly = TRUE)) stop("Package 'survey' is required.")

args <- commandArgs(trailingOnly = FALSE)
script_path <- sub("^--file=", "", args[grep("^--file=", args)][1])
project_dir <- normalizePath(file.path(dirname(script_path), "../.."), mustWork = TRUE)
derived_dir <- file.path(project_dir, "02_data", "derived")
results_dir <- file.path(project_dir, "04_outputs", "results")
models_dir <- file.path(project_dir, "03_analysis", "models")
dir.create(results_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(models_dir, recursive = TRUE, showWarnings = FALSE)

data <- utils::read.csv(file.path(derived_dir, "harmonized_analysis_data.csv"),
                        stringsAsFactors = FALSE, na.strings = c("", "NA"))
for (v in c("sex", "race_ethnicity", "cycle", "education", "smoking")) {
  data[[v]] <- factor(data[[v]])
}
logical_vars <- c(
  "eligible", "primary_domain", "metabolic_dysfunction",
  "metabolic_dysfunction_single_lipid_med", "metabolic_dysfunction_measured",
  "mets", "high_tg", "low_hdl", "high_bp", "high_glucose"
)
for (v in intersect(logical_vars, names(data))) {
  if (is.character(data[[v]])) data[[v]] <- data[[v]] == "TRUE"
}

options(survey.lonely.psu = "adjust")
fasting <- data[!is.na(data$pooled_fasting_weight) &
                  data$pooled_fasting_weight > 0 &
                  !is.na(data$SDMVSTRA) & !is.na(data$SDMVPSU), ]
design_all <- survey::svydesign(
  ids = ~SDMVPSU,
  strata = ~SDMVSTRA,
  weights = ~pooled_fasting_weight,
  nest = TRUE,
  data = fasting
)
design_primary <- subset(design_all, primary_domain)

primary_formula <- metabolic_dysfunction ~ log_ltr_z * sex +
  splines::ns(RIDAGEYR, df = 3) + race_ethnicity + cycle +
  education + INDFMPIR + smoking + total_fmi
primary_model <- survey::svyglm(
  primary_formula, design = design_primary,
  family = quasipoisson(link = "log")
)
saveRDS(primary_model, file.path(models_dir, "primary_survey_model.rds"))

coef_table <- function(model, analysis_name) {
  sm <- summary(model)$coefficients
  critical_value <- stats::qt(0.975, df = model$df.residual)
  data.frame(
    analysis = analysis_name,
    term = rownames(sm),
    estimate = sm[, 1],
    standard_error = sm[, 2],
    statistic = sm[, 3],
    p_value = sm[, 4],
    exponentiated = exp(sm[, 1]),
    ci_low = exp(sm[, 1] - critical_value * sm[, 2]),
    ci_high = exp(sm[, 1] + critical_value * sm[, 2]),
    row.names = NULL
  )
}

sex_slopes <- function(model, analysis_name, exposure = "log_ltr_z") {
  b <- stats::coef(model)
  v <- stats::vcov(model)
  interaction_names <- intersect(c(paste0(exposure, ":sexWomen"), paste0("sexWomen:", exposure)), names(b))
  if (!exposure %in% names(b) || length(interaction_names) != 1) return(data.frame())
  interaction <- interaction_names[1]
  contrast <- rbind(
    Men = setNames(as.numeric(names(b) == exposure), names(b)),
    Women = setNames(as.numeric(names(b) == exposure | names(b) == interaction), names(b)),
    Interaction = setNames(as.numeric(names(b) == interaction), names(b))
  )
  estimate <- as.numeric(contrast %*% b)
  se <- sqrt(diag(contrast %*% v %*% t(contrast)))
  critical_value <- stats::qt(0.975, df = model$df.residual)
  data.frame(
    analysis = analysis_name,
    contrast = rownames(contrast),
    log_prevalence_ratio = estimate,
    standard_error = se,
    prevalence_ratio = exp(estimate),
    ci_low = exp(estimate - critical_value * se),
    ci_high = exp(estimate + critical_value * se),
    p_value = 2 * stats::pt(-abs(estimate / se), df = model$df.residual),
    row.names = NULL
  )
}

primary_coefficients <- coef_table(primary_model, "primary")
primary_contrasts <- sex_slopes(primary_model, "primary")
utils::write.csv(primary_coefficients, file.path(results_dir, "primary_model_coefficients.csv"),
                 row.names = FALSE)
utils::write.csv(primary_contrasts, file.path(results_dir, "primary_sex_contrasts.csv"),
                 row.names = FALSE)

sensitivity_metadata <- list()
sensitivity_contrasts <- list()
fit_sensitivity <- function(name, formula, condition) {
  condition_expr <- substitute(condition)
  keep <- eval(condition_expr, envir = design_all$variables, enclos = parent.frame())
  keep[is.na(keep)] <- FALSE
  d <- design_all[keep, ]
  model <- try(survey::svyglm(formula, design = d, family = quasipoisson(link = "log")),
               silent = TRUE)
  if (inherits(model, "try-error")) {
    return(data.frame(
      analysis = name, term = "MODEL_FAILED", estimate = NA, standard_error = NA,
      statistic = NA, p_value = NA, exponentiated = NA, ci_low = NA, ci_high = NA
    ))
  }
  saveRDS(model, file.path(models_dir, paste0("sensitivity_", name, ".rds")))
  mf <- model.frame(model)
  sensitivity_metadata[[name]] <<- data.frame(analysis=name, n=nrow(mf),
    cases=sum(model.response(mf)), men=sum(mf$sex=="Men"), women=sum(mf$sex=="Women"),
    male_cases=sum(model.response(mf)[mf$sex=="Men"]), female_cases=sum(model.response(mf)[mf$sex=="Women"]))
  exposures <- intersect(c("log_ltr_z", "scale(log(ag_ratio))", "scale(vat_kg)", "scale(leg_fmi)", "scale(trunk_fmi)"), names(coef(model)))
  sensitivity_contrasts[[name]] <<- do.call(rbind, lapply(exposures, function(x) {
    out <- sex_slopes(model, name, x); out$exposure <- x; out
  }))
  coef_table(model, name)
}

full_adjustment <- paste(
  "log_ltr_z * sex + splines::ns(RIDAGEYR, df = 3) +",
  "race_ethnicity + cycle + education + INDFMPIR + smoking"
)

sensitivities <- list(
  fit_sensitivity("unadjusted", metabolic_dysfunction ~ log_ltr_z * sex, primary_domain),
  fit_sensitivity(
    "measured_only_outcome",
    stats::as.formula(paste("metabolic_dysfunction_measured ~", full_adjustment, "+ total_fmi")),
    primary_domain & !is.na(metabolic_dysfunction_measured)
  ),
  fit_sensitivity(
    "single_count_lipid_medication",
    stats::as.formula(paste(
      "metabolic_dysfunction_single_lipid_med ~",
      full_adjustment, "+ total_fmi"
    )),
    primary_domain & !is.na(metabolic_dysfunction_single_lipid_med)
  ),
  fit_sensitivity(
    "conventional_mets",
    stats::as.formula(paste("mets ~", full_adjustment, "+ total_fmi")),
    primary_domain & !is.na(mets)
  ),
  fit_sensitivity(
    "bmi_adjusted",
    stats::as.formula(paste("metabolic_dysfunction ~", full_adjustment, "+ BMXBMI")),
    primary_domain & !is.na(BMXBMI)
  ),
  fit_sensitivity(
    "minimal_covariates",
    metabolic_dysfunction ~ log_ltr_z * sex +
      splines::ns(RIDAGEYR, df = 3) + race_ethnicity + cycle + total_fmi,
    primary_domain
  ),
  fit_sensitivity(
    "exclude_2017_2018",
    stats::as.formula(paste("metabolic_dysfunction ~", full_adjustment, "+ total_fmi")),
    primary_domain & cycle != "2017-2018"
  ),
  fit_sensitivity(
    "android_gynoid",
    metabolic_dysfunction ~ scale(log(ag_ratio)) * sex +
      splines::ns(RIDAGEYR, df = 3) + race_ethnicity + cycle +
      education + INDFMPIR + smoking + total_fmi,
    primary_domain & !is.na(ag_ratio) & ag_ratio > 0
  ),
  fit_sensitivity(
    "visceral_adipose_tissue",
    metabolic_dysfunction ~ scale(vat_kg) * sex +
      splines::ns(RIDAGEYR, df = 3) + race_ethnicity + cycle +
      education + INDFMPIR + smoking + total_fmi,
    primary_domain & !is.na(vat_kg) & vat_kg > 0
  ),
  fit_sensitivity(
    "leg_and_trunk_components",
    metabolic_dysfunction ~ scale(leg_fmi) * sex + scale(trunk_fmi) * sex +
      splines::ns(RIDAGEYR, df = 3) + race_ethnicity + cycle +
      education + INDFMPIR + smoking,
    primary_domain & !is.na(leg_fmi) & !is.na(trunk_fmi)
  )
)
sensitivity_table <- do.call(rbind, sensitivities)
utils::write.csv(sensitivity_table, file.path(results_dir, "sensitivity_model_coefficients.csv"),
                 row.names = FALSE)

component_outcomes <- c("high_tg", "low_hdl", "high_bp", "high_glucose")
component_results <- lapply(component_outcomes, function(outcome) {
  formula <- stats::as.formula(paste(outcome, "~", full_adjustment, "+ total_fmi"))
  model <- survey::svyglm(
    formula,
    design = design_primary,
    family = quasipoisson(link = "log")
  )
  result <- sex_slopes(model, paste0("component_", outcome))
  result$outcome <- outcome
  result
})
component_results <- do.call(rbind, component_results)
interaction_rows <- component_results$contrast == "Interaction"
component_results$p_value_fdr <- NA_real_
component_results$p_value_fdr[interaction_rows] <- stats::p.adjust(
  component_results$p_value[interaction_rows],
  method = "BH"
)
utils::write.csv(
  component_results,
  file.path(results_dir, "secondary_component_sex_contrasts.csv"),
  row.names = FALSE
)

nonlinear_model <- survey::svyglm(
  metabolic_dysfunction ~
    (log_ltr_z + I(log_ltr_z^2) + I(log_ltr_z^3)) * sex +
    splines::ns(RIDAGEYR, df = 3) + race_ethnicity + cycle +
    education + INDFMPIR + smoking + total_fmi,
  design = design_primary,
  family = quasipoisson(link = "log")
)
saveRDS(nonlinear_model, file.path(models_dir, "nonlinear_survey_model.rds"))
nonlinear_overall_test <- survey::regTermTest(
  nonlinear_model,
  ~I(log_ltr_z^2) + I(log_ltr_z^3) +
    I(log_ltr_z^2):sex + I(log_ltr_z^3):sex
)
nonlinear_main_test <- survey::regTermTest(
  nonlinear_model,
  ~I(log_ltr_z^2) + I(log_ltr_z^3)
)
nonlinear_interaction_test <- survey::regTermTest(
  nonlinear_model,
  ~I(log_ltr_z^2):sex + I(log_ltr_z^3):sex
)
nonlinear_tests <- rbind(
  data.frame(
    test = "joint quadratic and cubic exposure terms across sexes",
    statistic = as.numeric(nonlinear_overall_test$Ftest),
    numerator_df = as.numeric(nonlinear_overall_test$df),
    denominator_df = as.numeric(nonlinear_overall_test$ddf),
    p_value = as.numeric(nonlinear_overall_test$p)
  ),
  data.frame(
    test = "joint quadratic and cubic exposure terms in male reference group",
    statistic = as.numeric(nonlinear_main_test$Ftest),
    numerator_df = as.numeric(nonlinear_main_test$df),
    denominator_df = as.numeric(nonlinear_main_test$ddf),
    p_value = as.numeric(nonlinear_main_test$p)
  ),
  data.frame(
    test = "additional quadratic and cubic exposure-by-sex terms",
    statistic = as.numeric(nonlinear_interaction_test$Ftest),
    numerator_df = as.numeric(nonlinear_interaction_test$df),
    denominator_df = as.numeric(nonlinear_interaction_test$ddf),
    p_value = as.numeric(nonlinear_interaction_test$p)
  )
)
utils::write.csv(
  nonlinear_tests,
  file.path(results_dir, "nonlinear_interaction_test.csv"),
  row.names = FALSE
)

table1 <- survey::svyby(
  ~RIDAGEYR + BMXBMI + BMXWAIST + total_fmi + leg_trunk_ratio +
    metabolic_dysfunction,
  ~sex, design_primary, survey::svymean, na.rm = TRUE, keep.var = TRUE
)
utils::write.csv(as.data.frame(table1), file.path(results_dir, "table1_weighted_summary.csv"),
                 row.names = FALSE)

weighted_mean_sd <- function(design, variable) {
  mean_fit <- survey::svymean(stats::as.formula(paste0("~", variable)), design, na.rm = TRUE)
  variance_fit <- survey::svyvar(stats::as.formula(paste0("~", variable)), design, na.rm = TRUE)
  c(mean = as.numeric(stats::coef(mean_fit)), sd = sqrt(as.numeric(stats::coef(variance_fit))))
}

weighted_percent <- function(design, expression) {
  indicator <- eval(substitute(expression), envir = design$variables, enclos = parent.frame())
  indicator_numeric <- as.numeric(indicator)
  as.numeric(stats::coef(survey::svymean(~indicator_numeric, design, na.rm = TRUE))) * 100
}

sex_designs <- lapply(levels(fasting$sex), function(group) {
  subset(design_primary, sex == group)
})
names(sex_designs) <- levels(fasting$sex)

continuous_characteristics <- c(
  RIDAGEYR = "Age, years",
  BMXBMI = "Body mass index, kg/m²",
  BMXWAIST = "Waist circumference, cm",
  INDFMPIR = "Poverty-income ratio",
  total_fmi = "Total fat-mass index, kg/m²",
  leg_trunk_ratio = "Leg-to-trunk fat-mass ratio"
)
publication_rows <- lapply(names(continuous_characteristics), function(variable) {
  summaries <- lapply(sex_designs, weighted_mean_sd, variable = variable)
  data.frame(
    characteristic = unname(continuous_characteristics[variable]),
    Men = sprintf("%.1f (%.1f)", summaries$Men["mean"], summaries$Men["sd"]),
    Women = sprintf("%.1f (%.1f)", summaries$Women["mean"], summaries$Women["sd"]),
    statistic = "weighted mean (weighted SD)"
  )
})
publication_rows <- c(
  list(data.frame(
    characteristic = "Unweighted sample, n",
    Men = format(sum(design_primary$variables$sex == "Men"), scientific = FALSE),
    Women = format(sum(design_primary$variables$sex == "Women"), scientific = FALSE),
    statistic = "unweighted n"
  )),
  publication_rows,
  list(data.frame(
    characteristic = "Metabolic dysfunction, n (weighted %)",
    Men = sprintf(
      "%d (%.1f%%)",
      sum(design_primary$variables$sex == "Men" &
            design_primary$variables$metabolic_dysfunction, na.rm = TRUE),
      weighted_percent(sex_designs$Men, metabolic_dysfunction)
    ),
    Women = sprintf(
      "%d (%.1f%%)",
      sum(design_primary$variables$sex == "Women" &
            design_primary$variables$metabolic_dysfunction, na.rm = TRUE),
      weighted_percent(sex_designs$Women, metabolic_dysfunction)
    ),
    statistic = "unweighted n (weighted %)"
  ))
)

category_definitions <- list(
  race_ethnicity = c(
    "1" = "Mexican American", "2" = "Other Hispanic",
    "3" = "Non-Hispanic White", "4" = "Non-Hispanic Black",
    "6" = "Non-Hispanic Asian", "7" = "Other or multiracial"
  ),
  education = c(
    "1" = "Less than ninth grade", "2" = "Ninth to eleventh grade",
    "3" = "High school graduate or GED", "4" = "Some college or associate degree",
    "5" = "College graduate or above"
  ),
  smoking = c("Never" = "Never", "Former" = "Former", "Current" = "Current")
)
category_headings <- c(
  race_ethnicity = "Ethnicity",
  education = "Education",
  smoking = "Smoking status"
)
for (variable in names(category_definitions)) {
  publication_rows <- c(
    publication_rows,
    list(data.frame(
      characteristic = category_headings[variable],
      Men = "",
      Women = "",
      statistic = "weighted %"
    ))
  )
  for (code in names(category_definitions[[variable]])) {
    men_percent <- weighted_percent(
      sex_designs$Men,
      as.character(get(variable)) == code
    )
    women_percent <- weighted_percent(
      sex_designs$Women,
      as.character(get(variable)) == code
    )
    publication_rows <- c(
      publication_rows,
      list(data.frame(
        characteristic = paste0("  ", category_definitions[[variable]][code]),
        Men = sprintf("%.1f%%", men_percent),
        Women = sprintf("%.1f%%", women_percent),
        statistic = "weighted %"
      ))
    )
  }
}
utils::write.csv(
  do.call(rbind, publication_rows),
  file.path(results_dir, "table1_publication.csv"),
  row.names = FALSE
)

factor_mode <- function(x) {
  levels(x)[which.max(tabulate(x, nbins = nlevels(x)))]
}
reference <- data.frame(
  log_ltr_z = seq(-2, 2, length.out = 81),
  RIDAGEYR = stats::median(fasting$RIDAGEYR[fasting$primary_domain], na.rm = TRUE),
  INDFMPIR = stats::median(fasting$INDFMPIR[fasting$primary_domain], na.rm = TRUE),
  total_fmi = stats::median(fasting$total_fmi[fasting$primary_domain], na.rm = TRUE)
)
reference <- reference[rep(seq_len(nrow(reference)), 2), ]
reference$sex <- factor(rep(c("Men", "Women"), each = 81), levels = levels(fasting$sex))
for (v in c("race_ethnicity", "cycle", "education", "smoking")) {
  reference[[v]] <- factor(factor_mode(fasting[[v]][fasting$primary_domain]),
                           levels = levels(fasting[[v]]))
}
prediction_matrix <- stats::model.matrix(
  stats::delete.response(primary_model$terms),
  reference,
  contrasts.arg = primary_model$contrasts,
  xlev = primary_model$xlevels
)
prediction_link <- as.numeric(prediction_matrix %*% stats::coef(primary_model))
prediction_se <- sqrt(rowSums((prediction_matrix %*% stats::vcov(primary_model)) *
                                prediction_matrix))
prediction_critical_value <- stats::qt(0.975, df = primary_model$df.residual)
reference$predicted_prevalence <- exp(prediction_link)
reference$ci_low <- exp(prediction_link - prediction_critical_value * prediction_se)
reference$ci_high <- exp(prediction_link + prediction_critical_value * prediction_se)
utils::write.csv(reference[c("log_ltr_z", "sex", "predicted_prevalence", "ci_low", "ci_high")],
                 file.path(results_dir, "adjusted_prediction_curve.csv"), row.names = FALSE)

diagnostics <- data.frame(
  metric = c("fasting_design_rows", "primary_domain_rows", "primary_cases",
             "primary_design_degrees_freedom", "primary_deviance", "primary_df_residual"),
  value = c(nrow(fasting), sum(fasting$primary_domain),
            sum(fasting$metabolic_dysfunction[fasting$primary_domain], na.rm = TRUE),
            survey::degf(design_primary), stats::deviance(primary_model),
            stats::df.residual(primary_model))
)
utils::write.csv(diagnostics, file.path(results_dir, "survey_diagnostics.csv"),
                 row.names = FALSE)

cat("Survey analysis complete:", sum(fasting$primary_domain), "participants.\n")

utils::write.csv(do.call(rbind,sensitivity_metadata), file.path(results_dir,"sensitivity_sample_sizes.csv"),row.names=FALSE)
utils::write.csv(do.call(rbind,sensitivity_contrasts), file.path(results_dir,"sensitivity_sex_contrasts.csv"),row.names=FALSE)
all_sex_test <- survey::regTermTest(nonlinear_model, ~log_ltr_z:sex + I(log_ltr_z^2):sex + I(log_ltr_z^3):sex)
nonlinear_tests <- rbind(nonlinear_tests, data.frame(test="all exposure-by-sex terms",statistic=as.numeric(all_sex_test$Ftest),numerator_df=as.numeric(all_sex_test$df),denominator_df=as.numeric(all_sex_test$ddf),p_value=as.numeric(all_sex_test$p)))
utils::write.csv(nonlinear_tests,file.path(results_dir,"nonlinear_interaction_test.csv"),row.names=FALSE)
X <- model.matrix(delete.response(nonlinear_model$terms),reference,contrasts.arg=nonlinear_model$contrasts,xlev=nonlinear_model$xlevels)
eta <- as.numeric(X %*% coef(nonlinear_model))
se <- sqrt(rowSums((X %*% vcov(nonlinear_model))*X))
crit <- qt(.975,nonlinear_model$df.residual)
reference$predicted_prevalence <- exp(eta)
reference$ci_low <- exp(eta-crit*se)
reference$ci_high <- exp(eta+crit*se)
utils::write.csv(reference,file.path(results_dir,"nonlinear_prediction_curve.csv"),row.names=FALSE)
utils::write.csv(data.frame(sex=design_primary$variables$sex,log_ltr_z=design_primary$variables$log_ltr_z,weight=design_primary$variables$pooled_fasting_weight),file.path(derived_dir,"exposure_distribution.csv"),row.names=FALSE)
for (label in c("primary", "nonlinear")) {
  m <- if(label=="primary") primary_model else nonlinear_model
  diagnostics <- rbind(diagnostics,data.frame(metric=paste0(label,c("_fitted_above_one","_max_fitted","_converged")),value=c(sum(fitted(m)>1),max(fitted(m)),m$converged)))
}
utils::write.csv(diagnostics,file.path(results_dir,"survey_diagnostics.csv"),row.names=FALSE)
