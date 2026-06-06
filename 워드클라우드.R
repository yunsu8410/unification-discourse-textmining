# 📌 필요한 패키지 설치
install.packages(c("wordcloud", "wordcloud2", "RColorBrewer"))

# 📌 패키지 로드
library(KoNLP)
library(wordcloud)
library(wordcloud2)
library(RColorBrewer)
library(dplyr)
library(stringr)
library(purrr)

# 📌 형태소 분석기 초기화
useNIADic()

# 📌 불용어 리스트
stopwords_kr <- c("통일", "교수", "연구", "진행", "기자", "토론", "자유", "문제", "관계", "위원",
                  "필요", "기자단", "대한", "정부", "관련", "한반도", "수", "이", "것",
                  "그", "더", "주장", "강조", "이후", "방안", "그리고", "이번", "통해",
                  "하기", "했다", "우리", "대해", "여러", "때문", "모든", "에서", "이하")

# 📌 CSV 불러오기 (크롤링.R 실행 후 생성된 파일)
blog_data <- read.csv("blog_articles.csv", stringsAsFactors = FALSE)

# 📌 명사 추출 및 빈도 계산
keyword_counts <- blog_data %>%
  mutate(nouns = map(content, extractNoun)) %>%
  unnest_longer(nouns) %>%
  filter(!nouns %in% stopwords_kr) %>%
  filter(nchar(nouns) >= 2) %>%
  count(nouns, sort = TRUE)

print(head(keyword_counts, 20))

# ── 1. wordcloud (기본) ───────────────────────────────────
set.seed(42)
wordcloud(
  words = keyword_counts$nouns,
  freq  = keyword_counts$n,
  min.freq    = 5,
  max.words   = 100,
  random.order = FALSE,
  colors       = brewer.pal(8, "Dark2"),
  scale        = c(4, 0.5)
)

# 📌 PNG 저장
png("wordcloud_basic.png", width = 800, height = 600, res = 100)
set.seed(42)
wordcloud(
  words = keyword_counts$nouns,
  freq  = keyword_counts$n,
  min.freq    = 5,
  max.words   = 100,
  random.order = FALSE,
  colors       = brewer.pal(8, "Dark2"),
  scale        = c(4, 0.5)
)
dev.off()
cat("wordcloud_basic.png 저장 완료\n")

# ── 2. wordcloud2 (인터랙티브) ────────────────────────────
wc_data <- keyword_counts %>%
  filter(n >= 5) %>%
  rename(word = nouns, freq = n)

wordcloud2(
  data  = wc_data,
  size  = 0.8,
  color = "random-dark",
  backgroundColor = "white"
)
