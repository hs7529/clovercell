from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Chrome 드라이버 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# URL 입력
url = "https://www.youtube.com/shorts"
driver.get(url)

# 명시적 대기 설정
wait = WebDriverWait(driver, 10)

"""
def search_info():
    # ID가 "channel-info"인 요소를 찾음
    channel_info = wait.until(
        EC.presence_of_element_located((By.ID, "channel-info"))
    )
    
    # channel-info 하위의 <a> 태그를 찾음
    a_tag = channel_info.find_element(By.TAG_NAME, "a")
    
    # <a> 태그의 href 속성 값(채널 URL)과 텍스트(채널 이름)를 가져오기
    channel_url = a_tag.get_attribute('href')  # 채널 URL
    
    # 출력
    print(f"Channel URL: {channel_url}")
    
"""



try:
    # 5초마다 순차적으로 ytd-reel-video-renderer 태그로 이동
    for i in range(16):  # 16개의 요소 탐색
        xpath = f"(//ytd-reel-video-renderer)[{i+1}]"  # i번째 ytd-reel-video-renderer 요소
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

        # 스크롤을 해당 요소로 이동
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        print(f"Scrolled to element {i+1}.")
        
        # 5초 대기 후 다음 요소로 이동
        time.sleep(5)

except Exception as e:
    print(f"Error: {e}")

finally:
    # 브라우저 닫기
    driver.quit()

