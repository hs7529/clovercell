from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 드라이버 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# URL 입력
driver.get('https://www.youtube.com/?gl=US/shorts')
wait = WebDriverWait(driver, 10)

# 다음 쇼츠로 이동하는 함수
def go_to_next_shorts():
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.ID, 'navigation-button-down')))
        next_button.click()
        print("------Clicked Down------")
        time.sleep(3)  # 클릭 후 잠시 대기하여 다음 쇼츠가 로드되도록 함
    except Exception as e:
        print(f"Error clicking the next button: {e}")

# 쇼츠 요소들을 찾고 href 값을 리스트로 모으는 함수
def find_element():
    all_hrefs = []  # 전체 href를 모으는 리스트
    
    try:
        for i in range(10):
            current_hrefs = []  # i 값에 따라 리스트 초기화

            # XPath로 요소를 기다림
            shorts = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="channel-info"]/a')))
            
            if shorts and isinstance(shorts, list):
                for short in shorts:
                    href = short.get_attribute('href')  # href 속성 가져오기
                    current_hrefs.append(href)  # 현재 i번째의 href 값 리스트에 추가
            
            # i번째가 끝난 후 한 번에 출력
            if current_hrefs:
                print(f"{i}번째 활성화된 링크들: {current_hrefs}")
            
            # 전체 리스트에 합침
            all_hrefs.extend(current_hrefs)
            
            go_to_next_shorts()  # 다음 요소로 이동하는 함수
            time.sleep(3)  # 3초 대기
        
    except Exception as e:
        print(f"Error: {e}")
        pass
    
    return all_hrefs

# 함수 실행
try:
    all_hrefs_collected = find_element()
    print(f"모든 href 링크들: {all_hrefs_collected}")  # 전체 리스트 출력
finally:
    driver.quit()
