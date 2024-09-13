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
driver.get("https://www.youtube.com/shorts")

# 대기 설정
wait = WebDriverWait(driver, 10)

# ID가 0, 1, 2, 3... 등으로 증가하는 쇼츠 컨테이너를 찾음
id_value = 0  # ID 값 시작
while True:
    try:
        # 동적 ID로 컨테이너 찾기
        shorts_container = wait.until(EC.presence_of_element_located((By.ID, str(id_value))))
        
        # 채널 이름 요소 찾기 (CSS 셀렉터 사용)
        channel_name_element = shorts_container.find_element(By.CSS_SELECTOR, "yt-formatted-string#text a")
        channel_name = channel_name_element.text  # 채널 이름 텍스트
        
        # href 속성 값 가져오기
        channel_href = channel_name_element.get_attribute("href")
        
        # 출력
        print(f"ID: {id_value}, 채널 이름: {channel_name}, 채널 URL: {channel_href}")
        
        # ID 값 증가
        id_value += 1
        
        # 임의의 대기 시간 (너무 빨리 조회되지 않도록 설정)
        time.sleep(1)
    
    except Exception as e:
        # 더 이상 해당 ID가 존재하지 않으면 종료
        print(f"ID {id_value}에서 오류 발생: {e}")
        break

# 브라우저 닫지 않고 유지
driver.quit()
