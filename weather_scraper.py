from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import sqlite3

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def get_city_info(link): #Use links from scraping to get more info on each city
    try:
        driver.get(link)
        city_weather = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
        results = []
        for row in city_weather:
            title = row.find_elements(By.CSS_SELECTOR, 'th')
            element = row.find_elements(By.CSS_SELECTOR, 'td')
            results.append({
                title[0].text : element[0].text
            })
        df = pd.DataFrame(results)
        return df
    except Exception as e:
        print(f"An exception occurred: {type(e).__name__} {e}")
    finally:
        driver.quit()

try:
    driver.get('https://www.timeanddate.com/weather/')
    weather_table = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
    results = []
    for row in weather_table: #get each row in the table
        city = row.find_elements(By.CSS_SELECTOR, 'td a')
        times = row.find_elements(By.CSS_SELECTOR, 'td.r')
        temps = row.find_elements(By.CSS_SELECTOR, 'td.rbi')
        info ={
            'City' : city[0].text,
            'Link' : city[0].get_attribute('href'),
            'Time' : times[0].text,
            'Temperature F': temps[0].text
        }
        results.append(info)
    df = pd.DataFrame(results)
    print(df.head())

## Clean Data 
    df['Temperature C'] = (df['Temperature F']-32) * (5/9)
    df['Time'] = pd.to_datetime(df['Time'], format='%A, %I:%M %p', errors='coerce')
    df.dropna(subset=['City', 'Temperature', 'Time'], inplace=True)
    df.drop_duplicates(subset='City', keep='first', inplace=True)

## Get smaller DFs for each city
    city_info = {}
    for row in df:
        small_df = get_city_info(row['Link'])
        city_info[row['City']] = small_df
    pd.DataFrame(city_info)
        

## Exporting Data
    df.to_csv('./World_Weather.csv')
    city_info.tocsv('./Cities.csv')
    try:
        with  sqlite3.connect('./World_Weather.csv') as conn: 
            cursor = conn.cursor()
    except sqlite3.Error as e:
        print(f'An error occurred: {e}')

except Exception as e:
    print(f"An exception occurred: {type(e).__name__} {e}")
finally:
    driver.quit()