#!/usr/bin/env Rscript

if (!requireNamespace("foreign", quietly = TRUE)) stop("Package 'foreign' is required.")

args <- commandArgs(trailingOnly = FALSE)
script_path <- sub("^--file=", "", args[grep("^--file=", args)][1])
project_dir <- normalizePath(file.path(dirname(script_path), "../.."), mustWork = TRUE)
raw_dir <- file.path(project_dir, "02_data", "raw_public")
derived_dir <- file.path(project_dir, "02_data", "derived")
manifests_dir <- file.path(project_dir, "02_data", "manifests")
results_dir <- file.path(project_dir, "04_outputs", "results")
dir.create(derived_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(manifests_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(results_dir, recursive = TRUE, showWarnings = FALSE)

cycles <- data.frame(
  cycle = c("2011-2012", "2013-2014", "2015-2016", "2017-2018"),
  suffix = c("G", "H", "I", "J"),
  stringsAsFactors = FALSE
)

read_component <- function(component, suffix, variables, required = TRUE) {
  path <- file.path(raw_dir, paste0(component, "_", suffix, ".xpt"))
  if (!file.exists(path)) {
    if (required) stop("Missing source file: ", path)
    out <- data.frame(SEQN = numeric())
    return(out)
  }
  data <- foreign::read.xport(path)
  keep <- intersect(c("SEQN", variables), names(data))
  data <- data[keep]
  if (anyDuplicated(data$SEQN)) stop("Duplicate SEQN in ", basename(path))
  data
}

join_seqn <- function(x, y) {
  if (!nrow(y)) return(x)
  overlap <- setdiff(intersect(names(x), names(y)), "SEQN")
  if (length(overlap)) y <- y[setdiff(names(y), overlap)]
  merge(x, y, by = "SEQN", all.x = TRUE, sort = FALSE)
}

mean_positive <- function(data, variables) {
  present <- intersect(variables, names(data))
  values <- as.matrix(data[present])
  values[values <= 0] <- NA_real_
  ans <- rowMeans(values, na.rm = TRUE)
  ans[rowSums(!is.na(values)) == 0] <- NA_real_
  ans
}

known_med <- function(history, treatment, negative_history = c(2)) {
  ifelse(
    treatment %in% 1, TRUE,
    ifelse(history %in% negative_history | treatment %in% 2, FALSE, NA)
  )
}

source(file.path(dirname(script_path), "data_rules.R"))

all_cycles <- list()
flow <- list()

for (i in seq_len(nrow(cycles))) {
  suffix <- cycles$suffix[i]
  cycle <- cycles$cycle[i]

  demo <- read_component("DEMO", suffix, c(
    "SDDSRVYR", "RIDSTATR", "RIAGENDR", "RIDAGEYR", "RIDRETH3", "RIDEXPRG",
    "DMDEDUC2", "INDFMPIR", "WTMEC2YR", "SDMVPSU", "SDMVSTRA"
  ))
  dxx <- read_component("DXX", suffix, c(
    "DXAEXSTS", "DXXLLFAT", "DXXRLFAT", "DXXTRFAT", "DXDTOFAT", "DXDTOPF"
  ))
  dxxag <- read_component("DXXAG", suffix, c(
    "DXXAGST", "DXXANFM", "DXXGYFM", "DXXAGRAT", "DXXVFATM", "DXXSATM"
  ))
  bmx <- read_component("BMX", suffix, c("BMXHT", "BMXWT", "BMXBMI", "BMXWAIST"))
  bpx <- read_component("BPX", suffix, c(paste0("BPXSY", 1:4), paste0("BPXDI", 1:4)))
  bpx$mean_sbp <- mean_positive(bpx, paste0("BPXSY", 1:4))
  bpx$mean_dbp <- mean_positive(bpx, paste0("BPXDI", 1:4))
  bpx <- bpx[c("SEQN", "mean_sbp", "mean_dbp")]
  hdl <- read_component("HDL", suffix, "LBDHDD")
  trigly <- read_component("TRIGLY", suffix, c("WTSAF2YR", "LBXTR"))
  glucose <- read_component("GLU", suffix, c("LBXGLU", "LBXIN"))
  insulin <- if (suffix == "G") glucose[c("SEQN", intersect("LBXIN", names(glucose)))] else
    read_component("INS", suffix, "LBXIN")
  ghb <- read_component("GHB", suffix, "LBXGH")
  biopro <- read_component("BIOPRO", suffix, c("LBXSATSI", "LBXSGTSI"))
  hscrp <- read_component("HSCRP", suffix, "LBXHSCRP", required = FALSE)
  bpq <- read_component("BPQ", suffix, c("BPQ020", "BPQ040A", "BPQ050A", "BPQ080", "BPQ090D", "BPQ100D"))
  diq <- read_component("DIQ", suffix, c("DIQ010", "DIQ050", "DIQ070"))
  smq <- read_component("SMQ", suffix, c("SMQ020", "SMQ040"))

  merged <- demo
  for (part in list(dxx, dxxag, bmx, bpx, hdl, trigly, glucose, insulin, ghb,
                    biopro, hscrp, bpq, diq, smq)) {
    merged <- join_seqn(merged, part)
  }

  merged$cycle <- cycle
  merged$sex <- factor(merged$RIAGENDR, c(1, 2), c("Men", "Women"))
  merged$female <- as.integer(merged$RIAGENDR == 2)
  merged$race_ethnicity <- factor(merged$RIDRETH3)
  merged$education <- factor(merged$DMDEDUC2)
  merged$smoking <- ifelse(
    merged$SMQ020 == 2, "Never",
    ifelse(merged$SMQ040 %in% c(1, 2), "Current",
           ifelse(merged$SMQ020 == 1 & merged$SMQ040 == 3, "Former", NA))
  )
  merged$smoking <- factor(merged$smoking, c("Never", "Former", "Current"))
  merged$pregnant <- !is.na(merged$RIDEXPRG) & merged$RIDEXPRG == 1
  merged$eligible <- merged$RIDSTATR == 2 & merged$RIDAGEYR >= 20 &
    merged$RIDAGEYR <= 59 & merged$WTMEC2YR > 0 & !merged$pregnant

  merged$dxa_valid <- merged$DXAEXSTS == 1 & merged$DXXLLFAT > 0 &
    merged$DXXRLFAT > 0 & merged$DXXTRFAT > 0 & merged$DXDTOFAT > 0 &
    merged$BMXHT > 0
  merged$leg_fat_g <- merged$DXXLLFAT + merged$DXXRLFAT
  merged$leg_trunk_ratio <- ifelse(
    merged$dxa_valid, merged$leg_fat_g / merged$DXXTRFAT, NA_real_
  )
  merged$log_leg_trunk_ratio <- log(merged$leg_trunk_ratio)
  merged$total_fmi <- (merged$DXDTOFAT / 1000) / (merged$BMXHT / 100)^2
  merged$leg_fmi <- (merged$leg_fat_g / 1000) / (merged$BMXHT / 100)^2
  merged$trunk_fmi <- (merged$DXXTRFAT / 1000) / (merged$BMXHT / 100)^2
  merged$ag_ratio <- ifelse(merged$DXXAGST == 1 & merged$DXXAGRAT > 0, merged$DXXAGRAT, NA)
  merged$vat_kg <- ifelse(merged$DXXAGST == 1 & merged$DXXVFATM > 0, merged$DXXVFATM / 1000, NA)

  merged$antihypertensive_med <- known_bpq_med(merged$BPQ020, merged$BPQ050A, merged$BPQ040A)
  merged$lipid_med_proxy <- known_bpq_med(merged$BPQ080, merged$BPQ100D, merged$BPQ090D)
  merged$insulin_med <- known_med(merged$DIQ010, merged$DIQ050, c(2, 3))
  merged$oral_diabetes_med <- known_med(merged$DIQ010, merged$DIQ070, c(2, 3))
  merged$diagnosed_diabetes <- ifelse(merged$DIQ010 %in% 1, TRUE,
                                      ifelse(merged$DIQ010 %in% c(2, 3), FALSE, NA))

  # R's three-valued OR preserves unequivocal positive findings.
  merged$high_tg <- merged$LBXTR >= 150 | merged$lipid_med_proxy
  merged$low_hdl <- ifelse(merged$female == 1, merged$LBDHDD < 50,
                            merged$LBDHDD < 40) | merged$lipid_med_proxy
  merged$high_bp <- merged$mean_sbp >= 130 | merged$mean_dbp >= 85 |
    merged$antihypertensive_med
  merged$high_glucose <- merged$LBXGLU >= 100 | merged$diagnosed_diabetes |
    merged$insulin_med | merged$oral_diabetes_med
  primary_components <- cbind(
    high_tg = merged$high_tg, low_hdl = merged$low_hdl,
    high_bp = merged$high_bp, high_glucose = merged$high_glucose
  )
  merged$metabolic_components_observed <- rowSums(!is.na(primary_components)) == 4
  merged$metabolic_component_count <- rowSums(primary_components, na.rm = TRUE)
  merged$metabolic_dysfunction <- ifelse(
    merged$metabolic_components_observed,
    merged$metabolic_component_count >= 2, NA
  )
  measured_tg_component <- ifelse(
    !is.na(merged$LBXTR), merged$LBXTR >= 150, NA
  )
  measured_hdl_component <- ifelse(
    !is.na(merged$LBDHDD),
    ifelse(merged$female == 1, merged$LBDHDD < 50, merged$LBDHDD < 40),
    NA
  )
  measured_lipid_count <- rowSums(
    cbind(measured_tg_component, measured_hdl_component),
    na.rm = TRUE
  )
  single_count_lipid_components <- pmax(
    measured_lipid_count,
    as.integer(merged$lipid_med_proxy)
  )
  single_count_components_observed <-
    !is.na(measured_tg_component) & !is.na(measured_hdl_component) &
    !is.na(merged$lipid_med_proxy) & !is.na(merged$high_bp) &
    !is.na(merged$high_glucose)
  merged$metabolic_dysfunction_single_lipid_med <- ifelse(
    single_count_components_observed,
    single_count_lipid_components + merged$high_bp + merged$high_glucose >= 2,
    NA
  )
  merged$central_obesity <- ifelse(
    !is.na(merged$BMXWAIST),
    ifelse(merged$female == 1, merged$BMXWAIST >= 88, merged$BMXWAIST >= 102), NA
  )
  five_components <- cbind(primary_components, central_obesity = merged$central_obesity)
  merged$mets <- ifelse(rowSums(!is.na(five_components)) == 5,
                        rowSums(five_components, na.rm = TRUE) >= 3, NA)

  measured_components <- cbind(
    merged$LBXTR >= 150,
    ifelse(merged$female == 1, merged$LBDHDD < 50, merged$LBDHDD < 40),
    merged$mean_sbp >= 130 | merged$mean_dbp >= 85,
    merged$LBXGLU >= 100
  )
  measured_components[is.na(cbind(
    merged$LBXTR, merged$LBDHDD, merged$mean_sbp + merged$mean_dbp, merged$LBXGLU
  ))] <- NA
  merged$metabolic_dysfunction_measured <- ifelse(
    rowSums(!is.na(measured_components)) == 4,
    rowSums(measured_components, na.rm = TRUE) >= 2, NA
  )
  merged$homa_ir <- ifelse(merged$LBXGLU > 0 & merged$LBXIN > 0,
                           merged$LBXGLU * merged$LBXIN / 405, NA)
  merged$pooled_fasting_weight <- merged$WTSAF2YR / 4

  covariate_complete <- complete.cases(
    merged[c("RIDAGEYR", "race_ethnicity", "education", "INDFMPIR",
             "smoking", "total_fmi", "sex", "cycle")]
  )
  merged$primary_domain <- merged$eligible & merged$dxa_valid &
    merged$pooled_fasting_weight > 0 & merged$metabolic_components_observed &
    covariate_complete
  merged$primary_domain[is.na(merged$primary_domain)] <- FALSE

  flow[[cycle]] <- data.frame(
    cycle = cycle,
    stage = c("MEC adults 20-59, not pregnant", "Positive fasting weight",
              "Valid required DXA", "All outcome components", "Primary complete"),
    n = c(
      sum(merged$eligible, na.rm = TRUE),
      sum(merged$eligible & merged$pooled_fasting_weight > 0, na.rm = TRUE),
      sum(merged$eligible & merged$pooled_fasting_weight > 0 & merged$dxa_valid, na.rm = TRUE),
      sum(merged$eligible & merged$pooled_fasting_weight > 0 & merged$dxa_valid &
            merged$metabolic_components_observed, na.rm = TRUE),
      sum(merged$primary_domain, na.rm = TRUE)
    )
  )
  all_cycles[[cycle]] <- merged
}

all_names <- unique(unlist(lapply(all_cycles, names)))
all_cycles <- lapply(all_cycles, function(x) {
  missing_names <- setdiff(all_names, names(x))
  for (name in missing_names) x[[name]] <- NA
  x[all_names]
})
data <- do.call(rbind, all_cycles)
rownames(data) <- NULL

primary <- data$primary_domain
w <- data$pooled_fasting_weight[primary]
x <- data$log_leg_trunk_ratio[primary]
weighted_mean <- sum(w * x) / sum(w)
weighted_sd <- sqrt(sum(w * (x - weighted_mean)^2) / sum(w))
data$log_ltr_z <- (data$log_leg_trunk_ratio - weighted_mean) / weighted_sd

keep <- c(
  "SEQN", "cycle", "SDDSRVYR", "SDMVSTRA", "SDMVPSU", "WTMEC2YR",
  "WTSAF2YR", "pooled_fasting_weight", "eligible", "primary_domain",
  "RIAGENDR", "sex", "female", "RIDAGEYR", "RIDRETH3", "race_ethnicity",
  "DMDEDUC2", "education", "INDFMPIR", "SMQ020", "SMQ040", "smoking",
  "BMXHT", "BMXWT", "BMXBMI", "BMXWAIST", "DXAEXSTS", "DXXAGST",
  "DXXLLFAT", "DXXRLFAT", "DXXTRFAT", "DXDTOFAT", "DXDTOPF",
  "leg_fat_g", "leg_trunk_ratio", "log_leg_trunk_ratio", "log_ltr_z",
  "total_fmi", "leg_fmi", "trunk_fmi", "DXXAGRAT", "ag_ratio",
  "DXXVFATM", "vat_kg", "mean_sbp", "mean_dbp", "LBDHDD", "LBXTR",
  "LBXGLU", "LBXGH", "LBXIN", "LBXHSCRP", "LBXSATSI", "LBXSGTSI",
  "BPQ020", "BPQ040A", "BPQ050A", "BPQ080", "BPQ090D", "BPQ100D",
  "antihypertensive_med", "lipid_med_proxy", "insulin_med",
  "oral_diabetes_med", "diagnosed_diabetes", "high_tg", "low_hdl",
  "high_bp", "high_glucose", "metabolic_component_count",
  "metabolic_dysfunction", "metabolic_dysfunction_single_lipid_med",
  "metabolic_dysfunction_measured",
  "central_obesity", "mets", "homa_ir"
)
keep <- intersect(keep, names(data))
utils::write.csv(data[keep], file.path(derived_dir, "harmonized_analysis_data.csv"),
                 row.names = FALSE, na = "")
utils::write.csv(do.call(rbind, flow), file.path(results_dir, "participant_flow.csv"),
                 row.names = FALSE)

source_manifest <- utils::read.csv(file.path(manifests_dir, "raw-public-file-manifest.csv"),
                                   stringsAsFactors = FALSE)
source_manifest <- source_manifest[source_manifest$download_status == "downloaded", ]
utils::write.csv(source_manifest, file.path(manifests_dir, "source_manifest.csv"),
                 row.names = FALSE, na = "")

quality <- data.frame(
  metric = c("rows_all_cycles", "primary_complete", "primary_women", "primary_men",
             "primary_cases", "raw_log_exposure_weighted_mean",
             "raw_log_exposure_weighted_sd",
             "duplicate_seqn", "nonpositive_primary_weights"),
  value = c(
    nrow(data), sum(primary), sum(primary & data$female == 1),
    sum(primary & data$female == 0),
    sum(data$metabolic_dysfunction[primary], na.rm = TRUE),
    weighted_mean, weighted_sd, sum(duplicated(data$SEQN)),
    sum(primary & data$pooled_fasting_weight <= 0, na.rm = TRUE)
  )
)
utils::write.csv(quality, file.path(results_dir, "data_quality_checks.csv"),
                 row.names = FALSE)

cat("Built harmonized data:", nrow(data), "rows;", sum(primary), "primary complete.\n")
