import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import re
import time

# 📌 기사 URL 리스트
urls = [
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223776053885&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223735432782&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223720192614&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223718385049&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223713310487&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223704138725&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223703799721&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223697391720&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223691954791&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223688302214&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223684346714&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223684346714&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223675858943&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223647416275&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223633251754&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223633236985&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223627065736&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223622549493&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223622225503&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223614701972&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223596934358&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223596956504&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223589596490&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223589616772&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223582595412&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223580016278&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223555563133&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223553966080&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223546241046&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
    "https://blog.naver.com/PostView.naver?blogId=gounikorea&logNo=223539316901&categoryNo=84&parentCategoryNo=84&from=thumbnailList",
]

# 📌 특수문자 제거 함수
def clean_text(text):
    return re.sub(r"[^\w가-힣\s]", "", text).strip()

# 📌 크롤링 결과 저장 리스트
blog_data = []
failed_urls = []

headers = {"User-Agent": "Mozilla/5.0"}

# 📌 크롤링 실행
for url in urls:
    print(f"크롤링 중: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = "UTF-8"
        soup = BeautifulSoup(response.text, "html.parser")

        # 📌 제목 크롤링
        title_tag = soup.select_one(".se-title-text")
        if not title_tag:
            title_tag = soup.select_one(".pcol1")
        if not title_tag:
            title_tag = soup.select_one("h3")
        title = clean_text(title_tag.get_text()) if title_tag else ""

        # 📌 날짜 크롤링
        date_tag = soup.select_one(".se_publishDate")
        if not date_tag:
            date_tag = soup.select_one(".date")
        post_date = date_tag.get_text(strip=True) if date_tag else str(date.today())

        # 📌 본문 크롤링
        content_tag = soup.select_one(".se-main-container")
        if not content_tag:
            content_tag = soup.select_one(".post-view")
        if not content_tag:
            content_tag = soup.select_one("#post-view")
        content = clean_text(content_tag.get_text()) if content_tag else ""

        print(f"제목: {title}")
        print(f"날짜: {post_date}")
        print(f"본문 일부: {content[:100]}")

        if not title or not content:
            failed_urls.append(url)
        else:
            blog_data.append({"date": post_date, "title": title, "content": content})

    except Exception as e:
        print(f"오류 발생: {e}")
        failed_urls.append(url)

    time.sleep(1)  # 서버 부하 방지

# 📌 결과 확인
df_blog = pd.DataFrame(blog_data)
print(df_blog)

print("\n크롤링 실패한 URL 목록:")
for u in failed_urls:
    print(u)

# 📌 CSV 저장
df_blog.to_csv("blog_articles.csv", index=False, encoding="utf-8-sig")
print("blog_articles.csv 저장 완료")
