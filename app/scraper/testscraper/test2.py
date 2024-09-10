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

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# URL 입력
driver.get('https://www.youtube.com/shorts')

# 명시적 대기 설정 (첫 번째 쇼츠 로드)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, 'ytd-reel-video-renderer')))

def check_is_active():
    try:
        # 특정 태그(ytd-reel-video-renderer)를 기다림
        element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'ytd-reel-video-renderer')))
        print("Found ytd-reel-video-renderer")

        # is-active 속성을 확인
        is_active = element.get_attribute('is-active')

        # is-active 속성이 존재하는지 확인
        if is_active is not None:
            print("The element has the 'is-active' attribute.")
            if is_active == 'True':
                print("The 'is-active' attribute is True. Scraping channel-info.")
                return True
            else:
                print(f"The 'is-active' attribute is not True: {is_active}")
        else:
            print("The element does not have the 'is-active' attribute.")
        
        return False

    except Exception as e:
        print(f"Error: {e}")
        return False

# 다음 쇼츠로 이동하는 함수
def go_to_next_shorts():
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.ID, 'navigation-button-down')))
        next_button.click()
        print("Clicked the navigation button to move to the next shorts.")
        time.sleep(3)  # 클릭 후 잠시 대기하여 다음 쇼츠가 로드되도록 함
    except Exception as e:
        print(f"Error clicking the next button: {e}")

# 메인 실행 로직
try:
    for _ in range(10):  # 최대 10번 시도
        if check_is_active():
            # is-active 속성이 True인 경우 작업 완료
            break
        else:
            go_to_next_shorts()  # is-active 속성이 False 또는 None이면 다음 쇼츠로 이동
finally:
    driver.quit()









from pytube import YouTube
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
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# URL 입력
driver.get('https://www.youtube.com/shorts')

# 요소가 로드될 때까지 명시적 대기 (첫 번째 쇼츠 로드)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, 'ytd-reel-video-renderer')))

# 'ytd-reel-video-renderer' 요소에서 is-active 속성 확인
def check_is_active():
    try:
        element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'ytd-reel-video-renderer')))
        print("Found ytd-reel-video-renderer")

        # is-active 속성 확인
        is_active = element.get_attribute('is-active')
        if is_active is not None and is_active.lower() == 'true':  # 대소문자 구분 없이 'true' 확인
            print("The 'is-active' attribute is True. Scraping channel-info.")
            return True
        else:
            print(f"The 'is-active' attribute is not True or missing: {is_active}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# 다음 쇼츠로 이동하는 함수
def go_to_next_shorts():
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.ID, 'navigation-button-down')))
        next_button.click()
        print("Clicked the navigation button to move to the next shorts.")
        time.sleep(3)  # 클릭 후 잠시 대기하여 다음 쇼츠가 로드되도록 함
    except Exception as e:
        print(f"Error clicking the next button: {e}")

# 쇼츠 정보를 직접 Selenium으로 추출하는 함수
def get_shorts_info():
    try:
        # 채널 정보 추출 (id가 'channel-name'인 요소를 사용)
        channel_info = driver.find_element(By.CSS_SELECTOR, "yt-formatted-string#channel-name")
        channel_name = channel_info.text
        print(f"Channel Name: {channel_name}")

        # 쇼츠 제목 및 조회수 정보 추출
        title = driver.find_element(By.CSS_SELECTOR, "h1.title").text
        views = driver.find_element(By.CSS_SELECTOR, "span.view-count").text
        print(f"Title: {title}")
        print(f"Views: {views}")

    except Exception as e:
        print(f"Error getting shorts info: {e}")

# 메인 실행 로직
try:
    for _ in range(5):  # 최대 5번 반복
        if check_is_active():
            print("Shorts Video Info:")
            get_shorts_info()  # is-active 속성이 True인 경우 작업 완료
        go_to_next_shorts()  # 다음 쇼츠로 이동
finally:
    driver.quit()








































from pytube import YouTube
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
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# URL 입력
driver.get('https://www.youtube.com/shorts')

# 요소가 로드될 때까지 명시적 대기 (첫 번째 쇼츠 로드)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, 'ytd-reel-video-renderer')))

# 'ytd-reel-video-renderer' 요소에서 is-active 속성 확인
def check_is_active():
    try:
        element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'ytd-reel-video-renderer')))
        print("Found ytd-reel-video-renderer")
        
        # is-active 속성을 확인
        is_active = element.get_attribute('is-active')
        
        if is_active is not None and is_active.lower() == 'true':  # 'true' 문자열 확인
            print("The 'is-active' attribute is True. Scraping shorts info.")
            return True
        else:
            print(f"The 'is-active' attribute is not active: {is_active}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# 다음 쇼츠로 이동하는 함수
def go_to_next_shorts():
    try:
        # 아래 버튼을 찾을 때까지 기다린 후 클릭
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#navigation-button-down')))
        next_button.click()
        print("Clicked the navigation button to move to the next shorts.")
        time.sleep(3)  # 클릭 후 잠시 대기하여 다음 쇼츠가 로드되도록 함
    except Exception as e:
        print(f"Error clicking the next button: {e}")

# 쇼츠 정보를 직접 Selenium으로 추출하는 함수
def get_shorts_info():
    try:
        # 채널 이름 및 쇼츠 정보 추출
        channel_info = driver.find_element(By.CSS_SELECTOR, 'yt-formatted-string#channel-name')
        channel_name = channel_info.text
        title = driver.find_element(By.CSS_SELECTOR, 'h1.title').text
        views = driver.find_element(By.CSS_SELECTOR, 'span.view-count').text
        
        print(f"Channel Name: {channel_name}")
        print(f"Title: {title}")
        print(f"Views: {views}")
    except Exception as e:
        print(f"Error getting shorts info: {e}")

# 메인 실행 로직
try:
    for _ in range(5):  # 최대 5번 반복
        if check_is_active():
            get_shorts_info()  # is-active 속성이 True인 경우 작업 완료
        go_to_next_shorts()  # 다음 쇼츠로 이동
finally:
    driver.quit()





from pytube import YouTube
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pytube import YouTube
import time

# Chrome 드라이버 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# URL 입력
driver.get('https://www.youtube.com/shorts')
wait = WebDriverWait(driver, 5)

# 'ytd-reel-video-renderer' 요소에서 is-active 속성 확인
def check_is_active():
    try:
        for i in range(10): 
            xpath = f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-shorts/div[3]/div[2]/ytd-reel-video-renderer[{i}]"
            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            # element = driver.find_element(By.XPATH, xpath)  # XPath로 요소 선택
            print(f"Element {i} found: {element.text}")
            is_active = element.get_attribute('is-active') # is-active 속성을 확인
            
            if is_active is not None:  
                print("is-active 활성화 >> Scraping shorts info.")
                get_shorts_info()  # is-active 속성이 True인 경우 작업 완료 
                go_to_next_shorts()  # 다음 쇼츠로 이동
            else:
                print("is-active 비활성 >>") 
                return False
    except Exception as e:
        print(f"Error: {e}")
        return False


# 다음 쇼츠로 이동하는 함수
def go_to_next_shorts():
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.ID, 'navigation-button-down')))
        next_button.click()
        print("------Clicked Down------")
        time.sleep(10)  # 클릭 후 잠시 대기하여 다음 쇼츠가 로드되도록 함
    except Exception as e:
        print(f"Error clicking the next button: {e}")
        
# 첫 번째 쇼츠 정보 가져오기
def get_shorts_info():
    try:
        # 채널 이름 및 쇼츠 정보 추출
        channel_info = driver.find_element(By.CSS_SELECTOR, 'yt-formatted-string#channel-name')
        print(channel_info.text)
        channel_name = channel_info.text
        title = driver.find_element(By.CSS_SELECTOR, 'h1.title').text
        views = driver.find_element(By.CSS_SELECTOR, 'span.view-count').text
        
        print(f"Channel Name: {channel_name}")
        print(f"Title: {title}")
        print(f"Views: {views}")
    except Exception as e:
        print(f"Error getting shorts info: {e}")
   


# 메인 실행 로직
try:
    for _ in range(5):  # 최대 5번 반복
        check_is_active()
finally:
    driver.quit()














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
driver.get('https://www.youtube.com/shorts')
wait = WebDriverWait(driver, 10)

# find elements
def find_element():
    for i in range(5):
        elements = wait.until(EC.presence_of_all_elements_located((By.ID, "channel-info")))
        
        # 각 요소를 순회하여 text 속성 출력
        for element in elements:
            print(element.text)
        
find_element()




for i in range(5):
            # xpath = f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-shorts/div[3]/div[2]/ytd-reel-video-renderer"
            # element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'ytd-reel-video-renderer')))
            time.sleep(5)
            print(f"{i}번쨰 : {element.text}")
            go_to_next_shorts()
            time.sleep(5)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
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
driver.get('https://www.youtube.com/shorts')
wait = WebDriverWait(driver, 10)


# 다음 쇼츠로 이동하는 함수
def go_to_next_shorts():
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.ID, 'navigation-button-down')))
        next_button.click()
        print("------Clicked Down------")
        time.sleep(5)  # 클릭 후 잠시 대기하여 다음 쇼츠가 로드되도록 함
    except Exception as e:
        print(f"Error clicking the next button: {e}")


# 쇼츠 요소들을 찾고 is-active 속성이 있는지 확인하는 함수
def find_element():
    try:
        for i in range(5):
            # 모든 'ytd-reel-video-renderer' 요소를 리스트로 저장
            elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'ytd-reel-video-renderer')))
            
            # 각 요소를 순회하면서 'is-active' 속성이 있는지 확인
            for element in elements:
                if element.get_attribute('is-active'):
                    print(f"Active element found: {element.text}")
            
            # 다음 쇼츠로 이동
            go_to_next_shorts()
            time.sleep(5)
    except Exception as e:
        print(f"Error: {e}")
        pass


find_element()





from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 드라이버 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.get('https://www.youtube.com/shorts')

# 대기 설정
wait = WebDriverWait(driver, 10)

# 모든 'ytd-reel-video-renderer' 요소를 가져옴
video_render = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'ytd-reel-video-renderer')))

# 모든 요소를 shorts 리스트로 저장
shorts = video_render

# 'is-active' 속성을 가진 요소 필터링
active_shorts = [short for short in shorts if short.get_attribute('is-active')]

# 필터링된 요소 출력
for active_short in active_shorts:
    print(f"Active short found: {active_short.text}")





# 모든 'ytd-reel-video-renderer' 요소가 로드될 때까지 대기
video_renderers = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'ytd-reel-video-renderer')))

# video_renderers는 리스트 형태로 반환됨
print(f"Number of video renderers found: {len(video_renderers)}")









from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# find_element 함수 정의
def find_element():
    try:
        for i in range(4):
            # 모든 'ytd-reel-video-renderer' 요소를 ID로 찾는 대신, XPath 또는 다른 방식을 사용해야 함
            shorts = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'ytd-reel-video-renderer')))
            
            # 'is-active' 속성이 있는지 확인
            active_shorts = [short for short in shorts if short.get_attribute('is-active')]

            if active_shorts:  # 활성화된 shorts가 있는 경우 출력
                for short in active_shorts:
                    print(f"{i}번째 : {short.text}")
            else:
                print(f"{i}번째 : 비활성화")

            # 다음 쇼츠로 이동
            go_to_next_shorts()
            time.sleep(3)

    except Exception as e:
        print(f"Error: {e}")
        pass

# 다음 쇼츠로 이동하는 함수 (예시 함수)
def go_to_next_shorts():
    # 쇼츠 페이지에서 다음 비디오로 이동하는 버튼을 찾는 로직 (예시)
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.ID, 'navigation-button-down')))
        next_button.click()
        print("다음 쇼츠로 이동 중...")
    except Exception as e:
        print(f"Error clicking the next button: {e}")

# WebDriverWait 설정 (이전 코드에서 WebDriver를 설정했다고 가정)
wait = WebDriverWait(driver, 10)

# 함수 실행
find_element()








from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# find_element 함수 정의
def find_element():
    try:
        for i in range(4):
            # 'ytd-reel-video-renderer' 태그의 모든 요소 찾기
            shorts = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'ytd-reel-video-renderer')))
            
            # 각 요소에 대해 'is-active' 속성 체크
            for short in shorts:
                # is-active 속성이 'true'로 설정될 때까지 기다림
                try:
                    wait.until(lambda driver: short.get_attribute('is-active') == 'true')
                    print(f"{i}번째 : {short.text} - 활성화됨")
                except Exception as e:
                    print(f"{i}번째 : 비활성화")

            # 다음 쇼츠로 이동
            go_to_next_shorts()
            time.sleep(3)

    except Exception as e:
        print(f"Error: {e}")
        pass

# 다음 쇼츠로 이동하는 함수 (예시 함수)
def go_to_next_shorts():
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.ID, 'navigation-button-down')))
        next_button.click()
        print("------Clicked Down------")
    except Exception as e:
        print(f"Error clicking the next button: {e}")

# WebDriverWait 설정 (이전 코드에서 WebDriver를 설정했다고 가정)
wait = WebDriverWait(driver, 10)

# 함수 실행
find_element()
