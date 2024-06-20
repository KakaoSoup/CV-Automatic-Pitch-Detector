from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from collections import namedtuple


# Set up ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL of the webpage to scrape
url = 'https://m.sports.naver.com/game/20240613LGSS02024/record'

# Open the webpage
driver.get(url)

# Optionally wait for the elements to load (adjust the time as needed)
driver.implicitly_wait(10)

try:
    # Find all div elements with the specified class
    score_divs = driver.find_elements(By.CLASS_NAME, 'TeamVS_score__2Iv0U')
    
    # Iterate over the found elements and print their text content
    for index, score_div in enumerate(score_divs, start=1):
        score = score_div.text
        print(f'Score {index}: {score}')
except Exception as e:
    print(f'Error: {e}')
finally:
    # Close the browser
    driver.quit()
