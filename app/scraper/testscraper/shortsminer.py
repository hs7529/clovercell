from selenium import webdriver
from bs4 import BeautifulSoup
from pytube import YouTube
import time

# 1. Selenium 설정 및 YouTube Shorts 페이지 접속
driver = webdriver.Chrome()  # 크롬 드라이버 경로 설정이 필요함
driver.get('https://www.youtube.com/shorts')

# YouTube 페이지가 완전히 로드될 때까지 기다림
time.sleep(5)  # 로딩 시간을 충분히 줘야 함

# 2. 페이지 소스 가져오기
html = driver.page_source

# 3. BeautifulSoup을 사용해 HTML 파싱
soup = BeautifulSoup(html, 'html.parser')

# 4. 쇼츠 컨테이너에서 각 쇼츠 URL 추출
shorts_containers = soup.find_all('a', {'id': 'thumbnail'})  # 쇼츠 링크를 포함하는 a 태그 찾기

shorts_links = []
for container in shorts_containers:
    link = 'https://www.youtube.com' + container['href']
    shorts_links.append(link)

# 5. pytube로 개별 쇼츠 링크에서 정보 추출
for link in shorts_links:
    try:
        yt = YouTube(link)
        print(f"Title: {yt.title}")
        print(f"Views: {yt.views}")
        print(f"Length: {yt.length} seconds")
    except Exception as e:
        print(f"Error processing {link}: {e}")

# Selenium 드라이버 종료
driver.quit()



# 유튜브 영상정보 가져오기
from pytube import YouTube

url = 'https://youtu.be/TtDeUBKpa6c'


yt = YouTube(url)

print("제목 : ", yt.title)
print("길이 : ", yt.length)
print("게시자 : ", yt.author)
print("게시날짜 : ", yt.publish_date)
print("조회수 : ", yt.views)
print("키워드 : ", yt.keywords)
print("설명 : ", yt.description)
print("썸네일 : ", yt.thumbnail_url)