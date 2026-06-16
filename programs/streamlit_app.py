import streamlit as st
import sqlite3
import pydeck as pdk
import pandas as pd

# Retrieve Data
with  sqlite3.connect("./weather_data.db") as conn:
    capitals = conn.query("SELECT * FROM Capitals__215;")
    most_popular = conn.query("SELECT * FROM Most_Popular__143;")
    least_popular = conn.query("SELECT * FROM Least_Popular__472;")
weather_data = st.connection("./db/weather_data.db", type="sql")

#Streamlit Set Up
st.title("International Weather Report")
st.header("Find the Weather in Your City")
with st.sidebar:
    st.header("Menu")

#Heat Map
COLOR_BREWER_BLUE_SCALE = [
    [240, 249, 232],
    [204, 235, 197],
    [168, 221, 181],
    [123, 204, 196],
    [67, 162, 202],
    [8, 104, 172],
]

popular_map = pdk.Layer(
    "HeatMapLayer",
    data = most_popular,
    get_position = ["longitude", "latitude"],
    color_range = COLOR_BREWER_BLUE_SCALE,
    get_weight = "temperature"
)
capitals_map = pdk.Layer(
    "HeatMapLayer",
    data = capitals,
    get_position =["longitude", "latitude"],
    color_range = COLOR_BREWER_BLUE_SCALE,
    get_weight = "temperature"
)
least_pop_map = pdk.Layer(
    "HeatMapLayer",
    data = least_popular,
    get_position = ["longitude", "latitude"],
    color_range = COLOR_BREWER_BLUE_SCALE,
    get_weight = "temperature"
)
r = pdk.Deck(
    layers=[popular_map,capitals_map,least_pop_map],
    initial_view_state=pdk.data_utils.compute_view(capitals[['Longitude','Latitude']]),
    map_provider="mapbox",
)
r.to_html("heatmap_layer.html")
