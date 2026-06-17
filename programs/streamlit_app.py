import streamlit as st
import pydeck as pdk
import pandas as pd
import plotly.express as px

def make_page(title, df):
    st.title(f"Temperature Data for {title}")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Most Common Heat (Farenheit)")
        fig1 = px.histogram(df,
                            x = "temperatureF",
                            title = "Most Common Heat World Wide (Farenheit)")
        fig1.write_html('common_heatF.html')
        st.plotly_chart(fig1)
    with col2:
        st.subheader("Most Common Heat (Celsius)")
        fig2 = px.histogram(df,
                            x = "temperatureC",
                            title = "Most Common Heat World Wide (Celsius)")
        fig2.write_html('common_heatC.html')
        st.plotly_chart(fig2)
    
    st.dataframe(df)

# Retrieve Data
conn = st.connection("weather_data",
                     type="sql",
                     url="sqlite:///weather_data.db")
capitals = conn.query("SELECT * FROM Capitals__215;", ttl=10)
most_popular = conn.query("SELECT * FROM Most_Popular__143;", ttl=10)
least_popular = conn.query("SELECT * FROM Somewhat_Popular__472;", ttl=10)

world_data = pd.concat([capitals, most_popular, least_popular]).drop_duplicates().reset_index(drop=True)
world_data['temperatureF'] = pd.to_numeric(world_data['temperatureF'], errors='coerce')
world_data['latitude'] = pd.to_numeric(world_data['latitude'], errors='coerce')
world_data['longitude'] = pd.to_numeric(world_data['longitude'], errors='coerce')
world_data.dropna(subset=['latitude', 'longitude', 'temperatureF'], inplace=True)


#Streamlit Set Up
st.title("International Weather Report")
st.header("Find the Weather in Your City")
city_name =st.text_input("City")
if city_name in world_data['city'].values:
    city_info = world_data[world_data['city'] == city_name].iloc[0]
    st.write(f"Temperature in {city_name}: {city_info['temperatureF']} °F / {city_info['temperatureC']} °C")
    st.write(f"Last Updated: {city_info['time']}")

with st.sidebar:
    st.header("Menu")
    view_mode = st.sidebar.selectbox("Select View Mode",
                                     ["World Data",
                                      "Capital Cities",
                                      "Most Popular Cities",
                                      "Least Popular Cities"])
    if view_mode == "World Data":
        df = world_data
    elif view_mode == "Capital Cities":
        df = capitals
    elif view_mode == "Most Popular Cities":
        df = most_popular
    elif view_mode == "Least Popular Cities":
        df = least_popular
    make_page(view_mode, df)