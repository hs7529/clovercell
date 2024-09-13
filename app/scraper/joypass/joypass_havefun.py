from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Chrome 드라이버 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--lang=ko")  # 한국어로 언어 설정

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# URL 입력
driver.get('https://www.travelcontentsapp.com/have-fun/')

wait = WebDriverWait(driver, 10)


joypasss = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div > div.cfToBox > div:nth-child(1) > div.cfToBox-item-txt'))) 
print(joypasss.text)

driver.quit()
