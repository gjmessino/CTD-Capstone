from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import sqlite3
from geopy.geocoders import Nominatim

def get_table_contents(link):
    try:
        driver.get(link)
        sleep(2)
        weather_table = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
        results = []
        for row in weather_table:
            cities = row.find_elements(By.CSS_SELECTOR, 'td a')
            times  = row.find_elements(By.CSS_SELECTOR, 'td.r')
            temps  = row.find_elements(By.CSS_SELECTOR, 'td.rbi')
            if not cities or not times or not temps:
                continue
            for i in range(len(cities)):  # iterate all columns in the row
                if i >= len(times) or i >= len(temps):
                    break
                info = {
                    'City':          cities[i].text,
                    'Link':          cities[i].get_attribute('href'),
                    'Time':          times[i].text,
                    'Temperature F': temps[i].text
                }
                results.append(info)
        df = pd.DataFrame(results)
        df = df.sort_values(by='City', ascending=True)
        return df
    except Exception as e:
        print(f"Failed to scrape {link}: {e}")
        return pd.DataFrame()

def get_alt_table(link):
    driver.get(link)
    table_options = driver.find_elements(By.CSS_SELECTOR, '#pop option')
    links_list = []
    for item in table_options:
        link_extend = item.get_attribute('value')
        new_link = (f"{link}?low={link_extend}")
        links_list.append([item.text,new_link])
    return links_list

def get_coords(city):
    sleep(1)
    try:
        loc = geolocator.geocode(city, timeout=10)  # increase to 10 seconds
        if loc:
            return pd.Series([loc.latitude, loc.longitude])
    except Exception:
        pass
    return pd.Series([None, None])

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                
try:
    main_link = "https://www.timeanddate.com/weather/"
    alt_links_list = get_alt_table(main_link)
    df_dict = {}
    for item in alt_links_list:
        title = item[0]
        df = get_table_contents(item[1])
        df_dict[title] = df
except Exception as e:
    print(f"An exception occurred: {type(e).__name__} {e}")
finally:
    driver.quit()

# Cleaning/Adding Data
geolocator = Nominatim(user_agent="weather_app")
    
for title, df in df_dict.items():  
    if df.empty:
        print(f"Skipping {title} — no data")
        continue
    df['Temperature F'] = df['Temperature F'].str.replace('°F', '', regex=False).str.strip()
    df['Temperature F'] = pd.to_numeric(df['Temperature F'], errors='coerce')
    df['Temperature C'] = (df['Temperature F'] - 32) * (5/9)

     # Replace your location block with this:
    df[['Longitude','Latitude']] = df['City'].apply(get_coords)

    df['Time'] = pd.to_datetime(df['Time'] + f' {pd.Timestamp.now().year}', format='%a %I:%M %p %Y', errors='coerce')
    df.dropna(subset=['City', 'Temperature F', 'Time', 'Longitude', 'Latitude'], inplace=True)
# Exporting Data to CSV
    csv_name = (f"./db/{title}.csv")
    df.to_csv(csv_name, index=False)
    table_name = "".join(c if c.isalnum() else "_" for c in title)
    table_name = table_name.strip("_")
       
# Make SQL
    try:
        with  sqlite3.connect("./weather_data.db") as conn: 
            cursor = conn.cursor()
            sql_statement = (f"""
                             CREATE TABLE IF NOT EXISTS {table_name} (
                             city TEXT PRIMARY KEY,
                             link TEXT,
                             time TEXT,
                             temperatureF FLOAT,
                             temperatureC FLOAT,
                             longitude FLOAT,
                             latitude FLOAT
                             )""")
            cursor.execute(sql_statement)
                
            sql_statement2 = (f"""
                              INSERT INTO {table_name}
                              (city,link,time,temperatureF,temperatureC,longitude,latitude)
                              VALUES (?,?,?,?,?,?,?)
                              """)
            for _, row in df.iterrows():
                cursor.execute(sql_statement2, (row['City'], 
                                                row['Link'], 
                                                str(row['Time']), 
                                                row['Temperature F'], 
                                                row['Temperature C'], 
                                                row['Longitude'], 
                                                row['Latitude']))
                
    except sqlite3.Error as e:
        print(f'An error occurred: {e}')