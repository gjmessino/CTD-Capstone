from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import sqlite3

def get_table_contents(link):
        driver.get(link)
        sleep(2)
        weather_table = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
        results = []
        for row in weather_table: #get each row in the table
            city = row.find_elements(By.CSS_SELECTOR, 'td a')
            times = row.find_elements(By.CSS_SELECTOR, 'td.r')
            temps = row.find_elements(By.CSS_SELECTOR, 'td.rbi')
            if not city or not times or not temps:
                continue
            info ={
                'City' : city[0].text,
                'Link' : city[0].get_attribute('href'),
                'Time' : times[0].text,
                'Temperature F': temps[0].text
            }
            results.append(info)
        df = pd.DataFrame(results)
        return df

def get_alt_table(link):
    driver.get(link)
    table_options = driver.find_elements(By.CSS_SELECTOR, '#pop option')
    links_list = []
    for item in table_options:
        link_extend = item.get_attribute('value')
        new_link = (f"{link}?low={link_extend}")
        links_list.append([item.text,new_link])
    return links_list

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                
try:
    main_link= "https://www.timeanddate.com/weather/"
    alt_links_list = get_alt_table(main_link)
    df_dict = {}
    for item in alt_links_list:
        title = item[0]
        df = get_table_contents(item[1])
        df_dict[title] = df
    df_dict['Most Popular'] = get_table_contents(main_link)

# Cleaning Data
    for title, df in df_dict.items():  
        df['Temperature F'] = df['Temperature F'].str.replace('°F', '', regex=False).str.strip()
        df['Temperature F'] = pd.to_numeric(df['Temperature F'], errors='coerce')
        df['Temperature C'] = (df['Temperature F'] - 32) * (5/9)

        df['Time'] = pd.to_datetime(df['Time'] + f' {pd.Timestamp.now().year}', format='%a %I:%M %p %Y', errors='coerce')
        df.dropna(subset=['City', 'Temperature F', 'Time'], inplace=True)
# Exporting Data to CSV
        csv_name = (f"./{title}.csv")
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
                                 temperatureF TEXT,
                                 temperatureC TEXT
                                 )""")
                cursor.execute(sql_statement)
                
                sql_statement2 = (f"""
                                  INSERT INTO {table_name}
                                  (city,link,time,temperatureF,temperatureC)
                                  VALUES (?,?,?,?,?)
                                  """)
                for _, row in df.iterrows():
                    cursor.execute(sql_statement2, (row['City'], row['Link'], str(row['Time']), row['Temperature F'], row['Temperature C']))
        except sqlite3.Error as e:
            print(f'An error occurred: {e}')

except Exception as e:
    print(f"An exception occurred: {type(e).__name__} {e}")
finally:
    driver.quit()