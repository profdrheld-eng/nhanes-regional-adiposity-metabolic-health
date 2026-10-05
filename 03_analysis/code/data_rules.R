# Direct current use takes precedence; distinguish structural skips from nonresponse.
known_bpq_med <- function(history, treatment, recommendation) {
  ifelse(treatment %in% 1, TRUE,
    ifelse(treatment %in% 2, FALSE,
      ifelse(is.na(treatment) & recommendation %in% 2, FALSE,
        ifelse(is.na(treatment) & is.na(recommendation) & history %in% 2, FALSE, NA))))
}
