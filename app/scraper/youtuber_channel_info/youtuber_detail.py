
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
import os
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

def ensure_about_url(url):
    """Ensure the URL ends with '/about'."""
    if not url.endswith('/about'):
        return url.rstrip('/') + '/about'
    return url

def wait_for_page_load(browser, timeout=20):
    """Wait for the page to completely load by checking the document readyState."""
    WebDriverWait(browser, timeout).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

def scrape_youtube_channel_data(url, browser):
    """Scrape data from a YouTube channel's about page."""
    # Ensure URL ends with '/about'
    url = ensure_about_url(url)

    links_section_selector = "#link-list-container a"
    additional_info_selector = "#additional-info-container .style-scope.ytd-about-channel-renderer tr td"

    try:
        # Navigate to the URL
        browser.get(url)

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
csv_input_filename = "./app/scraper/youtuber_channel_info/csv/youtube_channels_input.csv"

urls = load_urls_from_csv(csv_input_filename)


# CSV 파일 이름 설정
csv_output_filename = "./app/scraper/youtuber_channel_info/csv/youtube_channels_info.csv"


# Initialize the browser
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--incognito")  # 시크릿 모드

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Open CSV file and write the data
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
