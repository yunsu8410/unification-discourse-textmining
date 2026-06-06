import pandas as pd
import matplotlib.pyplot as plt
import re

# 📌 한글 폰트 설정 (Windows 기준)
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 📌 CSV 불러오기
df_blog = pd.read_csv("blog_articles.csv", encoding="utf-8-sig")

# 📌 날짜 변환
df_blog["date"] = pd.to_datetime(df_blog["date"], format="%Y-%m-%d", errors="coerce")
df_blog = df_blog.dropna(subset=["date"])

print(df_blog["date"].unique())
print(df_blog.dtypes)

# 📌 특정 키워드 리스트
keywords = ["교육", "인권", "미국", "평화", "경제", "트럼프", "독트린", "안보", "815", "탈북민"]

# 📌 키워드별 날짜별 빈도 계산
records = []
for _, row in df_blog.iterrows():
    content = str(row["content"])
    for kw in keywords:
        count = content.count(kw)
        if count > 0:
            records.append({"date": row["date"], "word": kw, "n": count})

trend_data = pd.DataFrame(records)

if not trend_data.empty:
    trend_data = trend_data.groupby(["date", "word"], as_index=False)["n"].sum()
    trend_data = trend_data.dropna(subset=["date"])

    # 📌 트렌드 그래프
    plt.figure(figsize=(12, 6))
    for kw in keywords:
        kw_data = trend_data[trend_data["word"] == kw]
        if not kw_data.empty:
            plt.plot(kw_data["date"], kw_data["n"], marker="o", linewidth=1.5, label=kw)

    plt.title("키워드별 등장 빈도 트렌드")
    plt.xlabel("날짜")
    plt.ylabel("등장 횟수")
    plt.legend(title="키워드")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("키워드_트렌드.png", dpi=150)
    plt.show()
    print("키워드_트렌드.png 저장 완료")
else:
    print("트렌드 데이터가 없습니다. 키워드 또는 날짜 데이터를 확인하세요.")
