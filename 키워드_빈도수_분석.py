import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from konlpy.tag import Okt
from collections import Counter
import re

# 📌 한글 폰트 설정 (Windows 기준)
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 📌 CSV 불러오기 (크롤링.py 실행 후 생성된 파일)
df_blog = pd.read_csv("blog_articles.csv", encoding="utf-8-sig")

# 📌 형태소 분석기 초기화
okt = Okt()

# 📌 불용어 리스트
stopwords_kr = {
    "통일", "교수", "연구", "진행", "기자", "토론", "자유", "문제", "관계", "위원",
    "필요", "기자단", "대한", "정부", "관련", "한반도", "수", "이", "것",
    "그", "더", "주장", "강조", "이후", "방안", "그리고", "이번", "통해",
    "하기", "했다", "우리", "대해", "여러", "때문", "모든", "에서", "이하"
}

# 📌 명사 추출 함수
def extract_nouns(text):
    if not isinstance(text, str):
        return []
    nouns = okt.nouns(text)
    return [n for n in nouns if len(n) >= 2 and n not in stopwords_kr]

# 📌 전체 본문에서 명사 추출 및 빈도 계산
all_nouns = []
for content in df_blog["content"]:
    all_nouns.extend(extract_nouns(content))

counter = Counter(all_nouns)

# 📌 30회 이상 등장한 키워드만 필터링
keyword_counts = pd.DataFrame(counter.most_common(), columns=["nouns", "n"])
keyword_counts = keyword_counts[keyword_counts["n"] >= 30].reset_index(drop=True)

print(keyword_counts)

# 📌 막대 그래프 시각화
plt.figure(figsize=(10, 8))
plt.barh(keyword_counts["nouns"], keyword_counts["n"], color="steelblue")
plt.xlabel("빈도수")
plt.ylabel("키워드")
plt.title("기사에서 가장 많이 등장한 주요 명사")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("키워드_빈도수.png", dpi=150)
plt.show()
print("키워드_빈도수.png 저장 완료")
