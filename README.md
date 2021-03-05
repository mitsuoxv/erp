Tf-idf analysis of the economic report of the president
================
Mitsuo Shiota
2020/2/27

-   [Motivation](#motivation)
-   [Libraries](#libraries)
-   [Preparation](#preparation)
    -   [Download and split](#download-and-split)
    -   [Extract text](#extract-text)
    -   [Transform a list of lists into a
        dataframe](#transform-a-list-of-lists-into-a-dataframe)
-   [How many pages in a report?](#how-many-pages-in-a-report)
-   [Tokenize and count most frequently used
    words](#tokenize-and-count-most-frequently-used-words)
-   [tf-idf (term frequency–inverse document frequency)
    analysis](#tf-idf-term-frequencyinverse-document-frequency-analysis)
-   [Top 10 words by year](#top-10-words-by-year)

Updated: 2021-03-05

## Motivation

I have found [“Text Mining Fedspeak” by Len
Kiefer](http://lenkiefer.com/2018/07/28/text-mining-fedspeak/), which
applies tidytext techniques to analyze the annual Federal Reserve
Monetary Policy Report, very interesting. Especially the td-idf analysis
part is fascinating, as it reveals what the Fed is talking abount most
by year. For example, they talked a lot about “iraq”, “war” and “sars”
in 2003, and “subprime” in 2007 and 2008. I could feel the history.

So I use the same techniques to analyze the economic report of the
president from 1947 to 2021.

## Libraries

As usual, I attach tidyverse package. I also attach tidytext package,
which provides text mining techniques.

## Preparation

### Download and split

I download the economic report of the president from 1947 to 2019 from
[FRASER by Federal Reserve Bank of
St. Louis](https://fraser.stlouisfed.org/title/45), and from 2020 to
2021 from [govinfo.gov](https://www.govinfo.gov/app/collection/erp/).

I first tried to download each pdf into a temporary file, and to extract
text by pdftools::pdf\_text(). But pdftools::pdf\_text() hangs, when it
tries the 2009 report. When I make the 2009 report smaller by excluding
appendixes, pdftools::pdf\_text works. So I changed my strategy. I
download all pdf files in the directory data/before\_split, split them,
and save the files, which exclude appendixes, in the directory
data/after\_split.

I have already downloaded the pdf files by download.py whose codes are
below. I appreciate the digitization works done by the Federal Reserve
Bank of St. Louis. My small complaint is URL inconsistency. Now
before\_split directory size is around 530MB.

Next I manually check which page starts Appendix A, split pdf files, and
save the files which exclude appendixes in the directory
data/after\_split. I have used split.py whose codes are below. Now
after\_split directory size is around 460MB.

### Extract text

I adapt pdftools::pdf\_text() to each file in the directory
data/after\_split. pdf\_text() returns a text by page in a list. After I
have done all files, I get the list by report, each of which is the list
by page.

There may be some pdf problems in the 2005 report. I check like below,
and it looks OK.

``` r
length(erp_list$`2005_excl_app`)
```

    ## [1] 185

``` r
str(erp_list$`2005_excl_app`)
```

    ##  chr [1:185] "Economic Report\nof the President\nTransmitted to the Congress February 2005\n    Together with the Annual Repo"| __truncated__ ...

As the Federal Reserve Bank of St. Louis added some signatures to its
digitization work, I remove them.

I save the list of lists in rdata format. The data size is 15MB.

``` r
save(erp_list, file = "data/erp.rdata")
```

### Transform a list of lists into a dataframe

First I transform a list of lists first into a list of dataframes whose
columns are “text”, “report” and “page.” Next I split text by line, and
add a column, “line.” When I finish every list and bind rows, I get a
dataframe. I replace “report” column with “year” column.

## How many pages in a report?

The number of pages increased significantly in recent years.

![](README_files/figure-gfm/plot_total_pages-1.png)<!-- -->

I check manually which pages are the president part, and not the CEA
(Council of Economic Advisers) part, in each report, and build
data.frame. In 1947-48 and 1954-61, the reports of are not clearly
separated between the president part, “The Economic Report of the
President”, and the CEA part, “The Annual Report of the Council of
Economic Advisers”, so I distinguish by my judegement. Basically I
specify the page of “To the Congress of the United States:” as the start
page of the president part.

The number of pages in the president part has been less than 10 since
1982, which was the first one signed by Reagan.

![](README_files/figure-gfm/plot_pres_pages-1.png)<!-- -->

## Tokenize and count most frequently used words

Now I am ready to utilize tidytext functions. I tokenize texts into
words, remove all words which contain non-alphabetical characters

``` r
erp_text <- erp_text_raw_df %>% 
  unnest_tokens(word, text) %>% 
  mutate(word = str_remove_all(word, "[^A-Za-z ]")) %>%
  filter(word != "")

erp_text
```

    ## # A tibble: 5,880,967 x 4
    ##     page  line  year word       
    ##    <int> <int> <int> <chr>      
    ##  1     1     1  1947 the        
    ##  2     1     1  1947 economic   
    ##  3     1     1  1947 report     
    ##  4     1     1  1947 of         
    ##  5     1     1  1947 the        
    ##  6     1     1  1947 president  
    ##  7     1     1  1947 transmitted
    ##  8     1     1  1947 to         
    ##  9     1     1  1947 the        
    ## 10     1     1  1947 congress   
    ## # … with 5,880,957 more rows

I count words. The result is uninteresting.

``` r
erp_text  %>%
  count(word, sort = TRUE) 
```

    ## # A tibble: 112,180 x 2
    ##    word       n
    ##    <chr>  <int>
    ##  1 the   379322
    ##  2 of    244032
    ##  3 and   175587
    ##  4 in    171352
    ##  5 to    157188
    ##  6 a      88192
    ##  7 for    66756
    ##  8 that   53841
    ##  9 is     45923
    ## 10 by     41013
    ## # … with 112,170 more rows

Next I exclude stop words which are “a”, “the”, and something like that.
The result is still boring, as I know the reports are about the economy.

``` r
erp_text  %>%
  anti_join(stop_words, by = "word")%>%
  count(word, sort = TRUE) 
```

    ## # A tibble: 111,533 x 2
    ##    word         n
    ##    <chr>    <int>
    ##  1 percent  31069
    ##  2 economic 22508
    ##  3 growth   20501
    ##  4 rate     17957
    ##  5 income   15871
    ##  6 tax      15520
    ##  7 federal  13010
    ##  8 rates    12169
    ##  9 labor    11924
    ## 10 prices   11834
    ## # … with 111,523 more rows

## tf-idf (term frequency–inverse document frequency) analysis

So I turn to tf-idf analysis, which scores high the words which appear
frequently in this year’s report, but seldom appear in the other years’
reports.

The highest score naturally goes to “covid” in 2021. The high score of
“https” is due to richer references in recent reports.

``` r
erp_textb <- erp_text %>% 
  count(year, word, sort = TRUE) %>% 
  bind_tf_idf(word, year, n) %>%
  arrange(desc(tf_idf))

erp_textb
```

    ## # A tibble: 554,117 x 6
    ##     year word         n      tf   idf  tf_idf
    ##    <int> <chr>    <int>   <dbl> <dbl>   <dbl>
    ##  1  2021 covid      464 0.00341  4.32 0.0147 
    ##  2  2020 opioids    295 0.00261  2.93 0.00766
    ##  3  2020 opioid     292 0.00259  2.93 0.00758
    ##  4  2018 cyber      351 0.00205  2.93 0.00601
    ##  5  2020 https      276 0.00245  2.12 0.00519
    ##  6  2021 https      274 0.00201  2.12 0.00426
    ##  7  2019 https      415 0.00191  2.12 0.00406
    ##  8  2021 pandemic   217 0.00159  2.53 0.00402
    ##  9  2018 https      316 0.00185  2.12 0.00391
    ## 10  1985 takeover    99 0.00122  2.93 0.00357
    ## # … with 554,107 more rows

## Top 10 words by year

Next I would like to show top 10 words by year. I tried several times,
and somewhat arbitrarily picked custom stop words. I prepare the plot
function for drawing.

``` r
custom_stop_words <- 
  bind_rows(tibble(word = c("gdp",
                            "gnp",
                            "box",
                            "cea",
                            "ceas",
                            "yr",
                            "fy",
                            "pdf", "http", "https"),
                   lexicon = c("custom")), 
            stop_words)

plot_tf_idf <- function(year_start, year_end) {
  erp_textb %>% 
    filter(year >= year_start, year <= year_end) %>% 
    anti_join(custom_stop_words, by="word") %>%
    mutate(word = reorder_within(word, tf_idf, year)) %>% 
    group_by(year) %>% 
    top_n(10, tf_idf) %>% 
    ungroup() %>% 
    ggplot(aes(word, tf_idf, fill = year)) +
    geom_col(show.legend = FALSE) +
    labs(x = NULL, y = "tf-idf") +
    facet_wrap(~ year, scales = "free", ncol = 5) +
    coord_flip() +
    scale_x_reordered()
}
```

Digitization is not perfect. When I search “inn” in 1956, I find some
axis parts of charts as “inn”. So, you may see some strange words below.
Also, be aware that the scale of the tf-idf axis is not the same across
years.

Anyway, can’t you feel the history?

I found “yen” and “japanese” in 1984, read the report, and found the
report complained a lot about the undervalued Japanese yen. The report
seems to have been the prelude to the Plaza Accord of 1985. That is a
history, or is it?

``` r
plot_tf_idf(1947, 1961)
```

![](README_files/figure-gfm/year_1947_1961-1.png)<!-- -->

``` r
plot_tf_idf(1962, 1976)
```

![](README_files/figure-gfm/year_1962_1976-1.png)<!-- -->

``` r
plot_tf_idf(1977, 1991)
```

![](README_files/figure-gfm/year_1977_1991-1.png)<!-- -->

``` r
plot_tf_idf(1992, 2006)
```

![](README_files/figure-gfm/year_1992_2006-1.png)<!-- -->

``` r
plot_tf_idf(2007, 2021)
```

![](README_files/figure-gfm/year_2007_2021-1.png)<!-- -->

EOL
