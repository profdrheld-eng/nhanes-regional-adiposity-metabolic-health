args <- commandArgs(trailingOnly=FALSE)
p <- sub('^--file=', '', args[grep('^--file=',args)][1])
if (as.character(getRversion()) != '4.6.0') stop('Expected R 4.6.0')
x <- read.csv(file.path(dirname(p),'r-required-versions.csv'))
for (i in seq_len(nrow(x))) {
  if (!requireNamespace(x$Package[i],quietly=TRUE) || packageVersion(x$Package[i]) != package_version(x$Version[i])) stop('Missing or mismatched R package: ',x$Package[i])
}
cat('PASS: R dependency versions match\n')
