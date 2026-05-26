from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    driver.get('https://www.timeanddate.com/weather/')
    sleep(2) # wait 2 seconds
    driver.get('https://www.timeanddate.com/weather/')
except Exception as e:
    print(f"An exception occurred: {type(e).__name__} {e}")

nav_bar = driver.find_element(By.CSS_SELECTOR, 'div.my-city__item')
local_url = nav_bar.get_attribute('href')

driver.quit()