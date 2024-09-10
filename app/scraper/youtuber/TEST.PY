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

# KEYWORD = "buy domain"

# 스크린샷 저장 폴더 생성
os.makedirs("screenshots", exist_ok=True)

#브라우저 열기
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
browser.get("https://vidiq.com/youtube-stats/top/country/gb/")

#구글 검색 실행
"""
search_bar = browser.find_element(By.CLASS_NAME, "gLFyf")
search_bar.send_keys(KEYWORD)
search_bar.send_keys(Keys.ENTER)

#구글 검색 결과 로드 대기
elements = "tr" ##검색할 CLASS 이름
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, elements)))
search_results = browser.find_elements(By.TAG_NAME, elements)

tags = search_results.find_elements(By.TAG_NAME,"td")
"""
try:
    tr_elements = browser.find_elements(By.CSS_SELECTOR, 'tr.cursor-pointer')

    for index in range(len(tr_elements)):
        # 페이지 이동 전 현재 URL 저장
        current_url = browser.current_url

        # <tr> 요소 다시 찾기
        tr_element = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'tr.cursor-pointer:nth-of-type({index + 1})'))
        )
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
                print(f"Link URL found: {link_url}")
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
    print(f"An error occurred: {e}")




# print(search_results)

#스크린샷 반복 시행
# for index, search_result in enumerate(search_results):
#     search_result.screenshot(f"screenshots/youtuber_result_{index}.png")

browser.quit()









from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 브라우저 열기
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
browser.get("https://vidiq.com/youtube-stats/top/country/us/")

try:
    # 모든 <tr> 요소를 가져오기 (cursor-pointer 클래스를 가진)
    tr_elements = browser.find_elements(By.CSS_SELECTOR, 'tr.cursor-pointer')
    
    for index, tr_element in enumerate(tr_elements):
        try:
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
            tr_element = WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'tr.cursor-pointer:nth-of-type({index + 1})'))
            )
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






















import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs

def extract_actual_url(youtube_redirect_url):
    """Extract the actual URL from a YouTube redirect URL."""
    parsed_url = urlparse(youtube_redirect_url)
    query_params = parse_qs(parsed_url.query)
    if 'q' in query_params:
        actual_url = query_params['q'][0]
        return actual_url
    else:
        return youtube_redirect_url  # 반환할 수 있는 'q' 매개변수가 없을 경우, 원래 URL 반환

def scrape_youtube_channel_data(url, browser):
    """Scrape data from a YouTube channel's about page."""
    links_section_selector = "#links-section a"
    additional_info_selector = "#additional-info-container .style-scope.ytd-about-channel-renderer tr td"

    try:
        # Navigate to the URL
        browser.get(url)

        # Wait for the #links-section to be present and get all href attributes
        try:
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, links_section_selector)))
            link_elements = browser.find_elements(By.CSS_SELECTOR, links_section_selector)
        except Exception as e:
            print(f"Failed to find elements in links section: {e}")
            link_elements = []

        # Extract and resolve any YouTube redirects
        link_urls = [extract_actual_url(element.get_attribute('href')) for element in link_elements]

        # Wait for the #additional-info-container to be present and get all td elements inside tr
        try:
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, additional_info_selector)))
            additional_info_elements = browser.find_elements(By.CSS_SELECTOR, additional_info_selector)
        except Exception as e:
            print(f"Failed to find elements in additional info section: {e}")
            additional_info_elements = []

        # Extract the text content of each td element
        additional_info_texts = [element.text.strip() for element in additional_info_elements]

        return [url] + [", ".join(link_urls)] + additional_info_texts  # Return the row data for CSV

    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")
        return [url, "Error occurred"]  # Return an error row if something goes wrong

# List of URLs
urls = [
    "https://www.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA/about",
    # Add more URLs here...
]

# CSV 파일 이름 설정
csv_filename = "youtube_channels_info.csv"

# Initialize the browser
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--incognito")  # 시크릿 모드

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Open CSV file and write the data
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Channel URL", "Link URLs", "Additional Info 1", "Additional Info 2", "Additional Info 3"])  # Example headers

    for url in urls:
        row_data = scrape_youtube_channel_data(url, browser)
        writer.writerow(row_data)

print(f"\nAll data has been written to {csv_filename}")

# Close the browser
browser.quit()














import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs

def extract_actual_url(youtube_redirect_url):
    """Extract the actual URL from a YouTube redirect URL."""
    parsed_url = urlparse(youtube_redirect_url)
    query_params = parse_qs(parsed_url.query)
    if 'q' in query_params:
        actual_url = query_params['q'][0]
        return actual_url
    else:
        return youtube_redirect_url  # 반환할 수 있는 'q' 매개변수가 없을 경우, 원래 URL 반환

def scrape_youtube_channel_data(url, browser):
    """Scrape data from a YouTube channel's about page."""
    links_section_selector = "a"  # More general selector to capture all links
    additional_info_selector = "#additional-info-container .style-scope.ytd-about-channel-renderer tr td"

    try:
        # Navigate to the URL
        browser.get(url)

        # Wait for the page to fully load by waiting for a known element on the page
        try:
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, additional_info_selector))
            )
        except Exception as e:
            print(f"Page did not load correctly: {e}")
            return [url, "Page load error"]

        # Now that the page is fully loaded, find all href attributes
        try:
            link_elements = browser.find_elements(By.CSS_SELECTOR, links_section_selector)
        except Exception as e:
            print(f"Failed to find elements in links section: {e}")
            link_elements = []

        # Extract and resolve any YouTube redirects
        link_urls = [extract_actual_url(element.get_attribute('href')) for element in link_elements if element.get_attribute('href')]

        # Find and get all td elements inside tr
        try:
            additional_info_elements = browser.find_elements(By.CSS_SELECTOR, additional_info_selector)
        except Exception as e:
            print(f"Failed to find elements in additional info section: {e}")
            additional_info_elements = []

        # Extract the text content of each td element
        additional_info_texts = [element.text.strip() for element in additional_info_elements]

        return [url] + [", ".join(link_urls)] + additional_info_texts  # Return the row data for CSV

    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")
        return [url, "Error occurred"]  # Return an error row if something goes wrong

# List of URLs
urls = [
    "https://www.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA/about",
    # Add more URLs here...
]

# CSV 파일 이름 설정
csv_filename = "youtube_channels_info.csv"

# Initialize the browser
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--incognito")  # 시크릿 모드

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Open CSV file and write the data
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Channel URL", "Link URLs", "Additional Info 1", "Additional Info 2", "Additional Info 3"])  # Example headers

    for url in urls:
        row_data = scrape_youtube_channel_data(url, browser)
        writer.writerow(row_data)

print(f"\nAll data has been written to {csv_filename}")

# Close the browser
browser.quit()







from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
import csv

def extract_actual_url(youtube_redirect_url):
    """Extract the actual URL from a YouTube redirect URL."""
    parsed_url = urlparse(youtube_redirect_url)
    query_params = parse_qs(parsed_url.query)
    if 'q' in query_params:
        actual_url = query_params['q'][0]
        return actual_url
    else:
        return youtube_redirect_url  # 반환할 수 있는 'q' 매개변수가 없을 경우, 원래 URL 반환

def wait_for_page_load(browser, timeout=30):
    """Wait for the page to completely load by checking the document readyState."""
    WebDriverWait(browser, timeout).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

def scrape_youtube_channel_data(url, browser):
    """Scrape data from a YouTube channel's about page."""
    links_section_selector = "#links-section a"
    additional_info_selector = "#additional-info-container .style-scope.ytd-about-channel-renderer tr td"

    try:
        # Navigate to the URL
        browser.get(url)

        # Wait for the page to fully load
        wait_for_page_load(browser)

        # Check if the #links-section is present
        try:
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, links_section_selector))
            )
        except Exception as e:
            print(f"Failed to find #links-section for {url}: {e}")
            return [url, "Links section not found"]

        # Now that the page is fully loaded, find all href attributes
        try:
            link_elements = browser.find_elements(By.CSS_SELECTOR, links_section_selector)
        except Exception as e:
            print(f"Failed to find elements in links section for {url}: {e}")
            link_elements = []

        # Extract and resolve any YouTube redirects
        link_urls = [extract_actual_url(element.get_attribute('href')) for element in link_elements if element.get_attribute('href')]

        # Find and get all td elements inside tr
        try:
            additional_info_elements = browser.find_elements(By.CSS_SELECTOR, additional_info_selector)
        except Exception as e:
            print(f"Failed to find elements in additional info section for {url}: {e}")
            additional_info_elements = []

        # Extract the text content of each td element
        additional_info_texts = [element.text.strip() for element in additional_info_elements]

        return [url] + [", ".join(link_urls)] + additional_info_texts  # Return the row data for CSV

    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")
        return [url, "Error occurred"]  # Return an error row if something goes wrong

# List of URLs
urls = [
    "https://www.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA/about",
    "https://www.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA",
    "https://www.youtube.com/channel/UCbCmjCuTUZos6Inko4u57UQ",
    "https://www.youtube.com/channel/UCk8GzjMOrta8yxDcKfylJYw"
    # Add more URLs here...
]

# CSV 파일 이름 설정
csv_filename = "youtube_channels_info.csv"

# Initialize the browser
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--incognito")  # 시크릿 모드

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Open CSV file and write the data
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Channel URL", "Link URLs", "Additional Info 1", "Additional Info 2", "Additional Info 3"])  # Example headers

    for url in urls:
        row_data = scrape_youtube_channel_data(url, browser)
        writer.writerow(row_data)

print(f"\nAll data has been written to {csv_filename}")

# Close the browser
browser.quit()




























































































import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs

def extract_actual_url(youtube_redirect_url):
    """Extract the actual URL from a YouTube redirect URL."""
    parsed_url = urlparse(youtube_redirect_url)
    query_params = parse_qs(parsed_url.query)
    if 'q' in query_params:
        actual_url = query_params['q'][0]
        return actual_url
    else:
        return youtube_redirect_url  # 반환할 수 있는 'q' 매개변수가 없을 경우, 원래 URL 반환

def ensure_about_url(url):
    """Ensure the URL ends with '/about'."""
    if not url.endswith('/about'):
        return url.rstrip('/') + '/about'
    return url

def wait_for_page_load(browser, timeout=30):
    """Wait for the page to completely load by checking the document readyState."""
    WebDriverWait(browser, timeout).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

def scrape_youtube_channel_data(url, browser):
    """Scrape data from a YouTube channel's about page."""
    # Ensure URL ends with '/about'
    url = ensure_about_url(url)

    links_section_selector = "#links-section a"
    additional_info_selector = "#additional-info-container .style-scope.ytd-about-channel-renderer tr td"

    try:
        # Navigate to the URL
        browser.get(url)

        # Wait for the page to fully load
        wait_for_page_load(browser)

        # Check if the #links-section is present
        try:
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, links_section_selector))
            )
        except Exception as e:
            print(f"Failed to find #links-section for {url}: {e}")
            return [url, "Links section not found"]

        # Now that the page is fully loaded, find all href attributes
        try:
            link_elements = browser.find_elements(By.CSS_SELECTOR, links_section_selector)
        except Exception as e:
            print(f"Failed to find elements in links section for {url}: {e}")
            link_elements = []

        # Extract and resolve any YouTube redirects
        link_urls = [extract_actual_url(element.get_attribute('href')) for element in link_elements if element.get_attribute('href')]

        # Find and get all td elements inside tr
        try:
            additional_info_elements = browser.find_elements(By.CSS_SELECTOR, additional_info_selector)
        except Exception as e:
            print(f"Failed to find elements in additional info section for {url}: {e}")
            additional_info_elements = []

        # Extract the text content of each td element
        additional_info_texts = [element.text.strip() for element in additional_info_elements]

        return [url] + [", ".join(link_urls)] + additional_info_texts  # Return the row data for CSV

    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")
        return [url, "Error occurred"]  # Return an error row if something goes wrong

def load_urls_from_csv(csv_filename):
    """Load URLs from a CSV file."""
    urls = []
    with open(csv_filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            urls.append(row['URL'])
    return urls

# Load URLs from an external CSV file
csv_input_filename = "youtube_channels.csv"
urls = load_urls_from_csv(csv_input_filename)

# CSV 파일 이름 설정
csv_output_filename = "youtube_channels_info.csv"

# Initialize the browser
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--incognito")  # 시크릿 모드

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Open CSV file and write the data
with open(csv_output_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Channel URL", "Link URLs", "Additional Info 1", "Additional Info 2", "Additional Info 3"])  # Example headers

    for url in urls:
        row_data = scrape_youtube_channel_data(url, browser)
        writer.writerow(row_data)

print(f"\nAll data has been written to {csv_output_filename}")

# Close the browser
browser.quit()











import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs

def extract_actual_url(youtube_redirect_url):
    """Extract the actual URL from a YouTube redirect URL."""
    parsed_url = urlparse(youtube_redirect_url)
    query_params = parse_qs(parsed_url.query)
    if 'q' in query_params:
        actual_url = query_params['q'][0]
        return actual_url
    else:
        return youtube_redirect_url  # 반환할 수 있는 'q' 매개변수가 없을 경우, 원래 URL 반환

def ensure_about_url(url):
    """Ensure the URL ends with '/about'."""
    if not url.endswith('/about'):
        return url.rstrip('/') + '/about'
    return url

def wait_for_page_load(browser, timeout=30):
    """Wait for the page to completely load by checking the document readyState."""
    WebDriverWait(browser, timeout).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

def scrape_youtube_channel_data(url, browser):
    """Scrape data from a YouTube channel's about page."""
    # Ensure URL ends with '/about'
    url = ensure_about_url(url)

    links_section_selector = "#links-section a"
    additional_info_selector = "#additional-info-container .style-scope.ytd-about-channel-renderer tr td"

    try:
        # Navigate to the URL
        browser.get(url)

        # Wait for the page to fully load
        wait_for_page_load(browser)

        # Check if the #links-section is present
        try:
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, links_section_selector))
            )
        except Exception as e:
            print(f"Failed to find #links-section for {url}: {e}")
            return [url, "Links section not found"]

        # Now that the page is fully loaded, find all href attributes
        try:
            link_elements = browser.find_elements(By.CSS_SELECTOR, links_section_selector)
        except Exception as e:
            print(f"Failed to find elements in links section for {url}: {e}")
            link_elements = []

        # Extract and resolve any YouTube redirects
        link_urls = [extract_actual_url(element.get_attribute('href')) for element in link_elements if element.get_attribute('href')]

        # Find and get all td elements inside tr
        try:
            additional_info_elements = browser.find_elements(By.CSS_SELECTOR, additional_info_selector)
        except Exception as e:
            print(f"Failed to find elements in additional info section for {url}: {e}")
            additional_info_elements = []

        # Extract the text content of each td element
        additional_info_texts = [element.text.strip() for element in additional_info_elements]

        return [url] + [", ".join(link_urls)] + additional_info_texts  # Return the row data for CSV

    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")
        return [url, "Error occurred"]  # Return an error row if something goes wrong

def load_urls_from_csv(csv_filename):
    """Load URLs from a CSV file."""
    urls = []
    with open(csv_filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            urls.append(row['URL'])
    return urls

# Load URLs from an external CSV file
csv_input_filename = "./csv/youtube_channels.csv"  # 경로를 실제 파일 위치로 수정
urls = load_urls_from_csv(csv_input_filename)

# CSV 파일 이름 설정
csv_output_filename = "youtube_channels_info.csv"

# Initialize the browser
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--incognito")  # 시크릿 모드

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Open CSV file in append mode and write the data
file_exists = os.path.isfile(csv_output_filename)
with open(csv_output_filename, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header only if the file doesn't exist
    if not file_exists:
        writer.writerow(["Channel URL", "Link URLs", "Additional Info 1", "Additional Info 2", "Additional Info 3"])  # Example headers

    for url in urls:
        row_data = scrape_youtube_channel_data(url, browser)
        writer.writerow(row_data)

print(f"\nAll data has been written to {csv_output_filename}")

# Close the browser
browser.quit()
