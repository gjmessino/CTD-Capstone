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

weather_table = driver.find_elements(By.CSS_SELECTOR, 'tbody')
results = []
for row in weather_table: #get each row in the table
    name_links = row.find_elements(By.CSS_SELECTOR, 'a')
    times = row.find_elements(By.CSS_SELECTOR, 'td.r')
    temps = row.find_elements(By.CSS_SELECTOR, 'td.rbi')
    for city in name_links: # break down 3 cities in each row
        link = city.get_attribute('href')
        location = city.text
        info= {"City" : location,
               "Link" : link}
        results.append(info)

df = pd.DataFrame(info)
print(df.head())
driver.quit()