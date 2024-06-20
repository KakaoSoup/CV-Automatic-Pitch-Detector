import time
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 전체 화면 캡처 기능을 정의하는 함수
def full_screenshot(driver, url, output_path):
    driver.get(url)  # 지정된 URL을 웹드라이버에서 열기.
    time.sleep(3)  # 페이지가 로드되기를 기다리기 위해 1초 동안 대기.

    # 자바스크립트를 실행하여 웹페이지의 총 높이를 가져오기.
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")

    # 브라우저 창을 페이지 하단으로 스크롤 하기.
    driver.execute_script("window.scrollTo(0, document.body.parentNode.scrollHeight);")

    time.sleep(1)  # 1초 동안 대기.

    # 창의 크기를 설정하여 전체 웹페이지를 캡처 (너비: 1920 픽셀, 높이: total_height 픽셀)
    driver.set_window_size("1920", total_height)

    time.sleep(1)  # 1초 동안 대기.
    driver.save_screenshot(output_path)  # 스크린샷을 지정된 출력 경로에 저장.
    
    
chrome_options = Options()
chrome_options.add_argument('--headless')

# web page
url = 'https://m.sports.naver.com/game/20240614SSNC02024/record'
# Chrome Web Driver
driver = webdriver.Chrome(options=chrome_options)
# output Path
output_path = "screenshot1.png"

full_screenshot(driver, url, output_path)

driver.quit()
