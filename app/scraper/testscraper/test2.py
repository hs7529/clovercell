from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Chrome 드라이버 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# YouTube Shorts 페이지로 이동
url = "https://www.youtube.com/shorts"
driver.get(url)

# 설정값
sizes = [480]
BROWSER_HEIGHT = 1066

for size in sizes:
    driver.set_window_size(size, BROWSER_HEIGHT)
    driver.execute_script("window.scrollTo(0,0)")
    time.sleep(3)
    
    last_scroll_size = 0  # 이전 스크롤 위치 저장
    new_scroll_size = driver.execute_script("return document.body.scrollHeight")  # 현재 스크롤 크기
    
    # 무한 스크롤 구현
    while True:
        # 페이지 끝까지 스크롤
        driver.execute_script(f"window.scrollTo(0, {new_scroll_size});")
        time.sleep(2)  # 페이지 로드를 기다리기 위해 짧은 시간 대기
        
        last_scroll_size = new_scroll_size
        new_scroll_size = driver.execute_script("return document.body.scrollHeight")
        
        # 새로운 콘텐츠가 로드되었는지 확인
        if new_scroll_size == last_scroll_size:
            print("더 이상 새로운 콘텐츠가 없습니다.")
            break  # 스크롤 크기가 변하지 않으면 반복문 종료
        
        # 특정 요소가 로드되었는지 확인 (YouTube Shorts 썸네일 예시)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'ytd-reel-video-renderer'))
            )
            print("새로운 동영상이 로드되었습니다.")
        except Exception as e:
            print("새로운 동영상 로드 실패 또는 시간 초과", e)
