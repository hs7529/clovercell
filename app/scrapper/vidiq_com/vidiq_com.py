from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--incognito")  # 시크릿 모드

#브라우저 열기
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
browser.get("https://vidiq.com/youtube-stats/top/country/ph/")

try:
    # 모든 <tr> 요소를 가져오기 (cursor-pointer 클래스를 가진)
    tr_elements = browser.find_elements(By.CSS_SELECTOR, 'tr.cursor-pointer')
    
    for index in range(len(tr_elements)):
        try:
            # 요소를 다시 찾아서 사용 (StaleElement 문제 방지)
            tr_element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'tr.cursor-pointer:nth-of-type({index + 1})'))
            )

            # 현재 <tr> 요소에서 td > span 텍스트 가져오기
            td_span_texts = []
            td_elements = tr_element.find_elements(By.CSS_SELECTOR, 'td > span')
 
            for td in td_elements:
                td_span_texts.append(td.text.strip())

            # 텍스트들을 ','로 구분하여 조합
            td_span_text_combined = ", ".join(td_span_texts)

            # 페이지 이동 전 현재 URL 저장
            current_url = browser.current_url

            # <tr> 요소 클릭
            tr_element.click()

            # 클릭 후 새 URL 확인을 위해 약간의 대기 추가
            WebDriverWait(browser, 20).until(EC.url_changes(current_url))

            # 클릭 후 이동된 URL 확인
            new_url = browser.current_url

            if new_url != current_url:
                try:
                    # Youtube URL을 가진 모든 링크를 찾음
                    link_element = WebDriverWait(browser, 20).until(
                        EC.presence_of_element_located((By.XPATH, 
                            "//div[contains(@class, 'order-2')]//a[@role='button' and contains(@href, 'youtube.com')]"))
                    )
                    link_url = link_element.get_attribute('href')
                    # 콤마로 구분된 텍스트와 URL 출력
                    combined_result = f"{td_span_text_combined}, {link_url}"
                    print(f"Row {index + 1} data: {combined_result}")
                except Exception as e:
                    print(f"Failed to retrieve the link on the new page: {e}")
            else:
                print(f"URL did not change after clicking tr {index + 1}. It might be a dynamic action or no URL is associated.")

            # 작업이 끝나면 다시 원래 페이지로 돌아갑니다.
            browser.back()

            # 원래 페이지로 돌아온 후 대기
            WebDriverWait(browser, 20).until(EC.url_to_be(current_url))

            # 다시 페이지로 돌아온 후 tr 요소들 갱신
            tr_elements = browser.find_elements(By.CSS_SELECTOR, 'tr.cursor-pointer')

        except Exception as e:
            print(f"Failed to process tr {index + 1}: {e}")

except Exception as e:
    print(f"An error occurred: {e}")






browser.quit()




