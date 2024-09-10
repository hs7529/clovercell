from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


#드라이버 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# URL 입력
driver.get('https://www.youtube.com/shorts')
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

# 쇼츠 요소들을 찾고 is-active 속성이 있는지 확인하는 함수
def find_element():
    try:
        for i in range(4):
            shorts = wait.until(EC.presence_of_all_elements_located((By.ID, f"{i}")))
            active_shorts = [short for short in shorts if short.get_attribute('is-active')]
            
            if active_shorts:  # 활성화된 shorts가 있는 경우 출력
                for short in active_shorts:
                    print(f"{i}번째 : {short.text}")
            else:
                print(f"{i}번째 : 비활성화")
                
            go_to_next_shorts()
            time.sleep(3)
            # print(short.text)
            # shorts = video_render
            # time.sleep(5)
            # active_shorts = [short for short in shorts if short.get_attribute('is-active')]
            
            # for short in active_shorts:
                
    except Exception as e:
        print(f"Error: {e}")
        pass


find_element()