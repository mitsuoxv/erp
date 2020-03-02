# This code fails as of February 2020: R 3.6.2, pdftools 2.3
# pdftools::pdf_text() hangs, when it deals with 2009 pdf

# library
library(tidyverse)

# function
extract_text <- function(url, page_range = NULL) {
  tf <- tempfile(fileext = ".pdf")
  
  httr::GET(url, httr::write_disk(tf))
  
  text <- pdftools::pdf_text(tf)
  
  if (!is.null(page_range)) {
    text <- text[page_range]
  }
  
  text 
}

# Appendix A start page by year
pages_by_year <- data.frame(
  year = 1947:2020,
  app_a_start = c(44, 98, 110,
                  134, 176, 160, 160, 126, 79, 109, 85, 85, 78,
                  84, 82, 199, 160, 173, 177,193, 204, 201, 218,
                  148, 171, 182, 147, 233, 224, 159, 176, 244, 169,
                  190, 220, 222, 152, 208, 223, 241, 233, 236, 297,
                  271, 270, 285, 331, 255, 251, 265, 286, 267, 312,
                  278, 245, 295, 251, 270, 186, 252, 203, 202, 261,
                  310, 170, 291, 303, 350, 370, 386, 549, 514, 619,
                  348)
)

# download and extract text
years <- pages_by_year$year
FRASER <- "https://fraser.stlouisfed.org/files/docs/publications/ERP/"

erp_list <- vector("list", length = nrow(pages_by_year))

for (i in seq_along(erp_list)) {
  year_chr <- as.character(pages_by_year$year[i])
  
  if (years[i] <= 1949) {
    # Although there are midyear reports from 1949 to 1952, I ignore them
    url <- str_c(FRASER,
                 year_chr, "/ERP_", year_chr, "_January.pdf")
  } else if (years[i] <= 1952) {
    url <- str_c(FRASER,
                 year_chr, "/ERP_January_", year_chr, ".pdf")
  } else if (years[i] <= 1986) {
    url <- str_c(FRASER,
                 year_chr, "/ERP_", year_chr, ".pdf")
  } else if (years[i] <= 1988) {
    url <- str_c(FRASER,
                 year_chr, "/ER_", year_chr, ".pdf")
  } else if (years[i] <= 2008) {
    url <- str_c(FRASER,
                 year_chr, "/ERP_", year_chr, ".pdf")
  } else if (years[i] == 2009) {
    url <- str_c(FRASER,
                 year_chr, "/", year_chr, "_ERP.pdf")
  } else if (years[i] == 2010) {
    url <- str_c(FRASER,
                 year_chr, "/erp_", year_chr, ".pdf")
  } else if (years[i] <= 2014) {
    url <- str_c(FRASER,
                 year_chr, "/", year_chr, "_erp.pdf")
  } else if (years[i] <= 2019) {
    url <- str_c(FRASER,
                 year_chr, "_erp.pdf")
  } else {
    url <- "https://www.whitehouse.gov/wp-content/uploads/2020/02/2020-Economic-Report-of-the-President-WHCEA.pdf"
  }
  
  erp_list[[i]] <- extract_text(
    url = url,
    page_range = 1:(pages_by_year$app_a_start[i] - 1)
  )
  
  print(year_chr)
  Sys.sleep(10) # I'm not attacking the server
}

names(erp_list) <- str_c(as.character(years), "_excl_app")

# remove signatures by the Federal Reserve Bank of St. Louis
remove_digitized <- function(report) {
  map(report,
      ~ str_remove(.x, "Digitized for FRASER") %>% 
        str_remove("http://fraser.stlouisfed.org/") %>% 
        str_remove("Federal Reserve Bank of St. Louis"))
}

erp_list <- map(erp_list, remove_digitized)

# save
save(erp_list, file = "data/erp2.rdata")


