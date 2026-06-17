This project looks at global weather data from the time and date website (https://www.timeanddate.com/weather/). Looking the table of
cities it used Selenium to scrape information about city name and temperature. It then incorporates Nominatim to geolocate each city 
to find its longitude and latitude. 

For data cleaning na lines were dropped, and formatting was standardized. I added a column for temperature conversion, so it would 
be listed both in celsius and farenheit.

The four table options from time and date were all made into their own CSV files, and a larger SQL database hosts the collection of
tables.

For the Streamlit app I created a heat map that shows a map of the world with a top layer displaying temperature for each city included
in the data. That's followed by two tables showing the distribution of global temperatures, one in Ferenheit the other in Celsius. The 
table of information is on display at the bottom.

With the side bar users can toggle through which data table they'd like to look at. They can also search their city (or any other) to 
find the temperature.
<img width="906" height="597" alt="Screenshot 2026-06-17 at 2 30 08 PM" src="<img width="344" height="403" alt="Screenshot 2026-06-17 at 2 30 24 PM" src="https://github.com/user-attachments/assets/b01c655f-8cb3-4798-a13a-e4a90d62e2d5" />" />

![Uploading Screenshot 2026-06-17 at 2.30.24 PM.png…]()

