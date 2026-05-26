from time import sleep
import pandas as pd
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

world_row = driver.get_elements(By.XPATH, '/html/body/div[5]/section[1]/div/section/div[1]/div/table/tbody/tr[1]')
for items in world_row:
    cities = items.get_elements(By.CSS_SELECTOR, 'a')
    print(cities.text)


driver.quit()