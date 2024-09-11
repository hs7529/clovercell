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
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# 유튜브 쇼츠 페이지 접속
driver.get('https://www.youtube.com/shorts')

# 명시적 대기 설정
wait = WebDriverWait(driver, 20)  # 대기 시간을 늘림

# 설정 메뉴 열기 (상단 우측 설정 버튼 클릭)
def open_settings():
    try:
        # 스크롤을 아래로 내림 (필요 시)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # 설정 버튼을 클릭 (설정 아이콘의 Xpath 또는 CSS 선택자를 확인 후 사용)
        settings_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Settings"]')))
        settings_button.click()
        print("Settings menu opened.")
        time.sleep(2)
    except Exception as e:
        print(f"Error opening settings: {e}")

# 위치 메뉴에서 '미국'을 선택하는 함수
def select_location():
    try:
        # '위치' 설정 메뉴 클릭
        location_menu = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Location"]')))
        location_menu.click()
        time.sleep(2)

        # '미국'을 선택 (미국 옵션의 XPath를 넣음)
        usa_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="subtitle" and text()="미국"]')))
        usa_option.click()
        print("Location set to USA.")
        time.sleep(2)

    except Exception as e:
        print(f"Error selecting location: {e}")

# 메인 실행 로직
try:
    open_settings()   # 설정 메뉴 열기
    select_location() # 지역을 '미국'으로 설정
finally:
    driver.quit()
