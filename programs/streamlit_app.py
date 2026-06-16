import streamlit as st
import pydeck as pdk
import pandas as pd
import plotly.express as px

# Retrieve Data
conn = st.connection("./weather_data.db","sql")
capitals = conn.query("SELECT * FROM Capitals__215;", ttl=600)
most_popular = conn.query("SELECT * FROM Most_Popular__143;", ttl=600)
least_popular = conn.query("SELECT * FROM Least_Popular__472;", ttl=600)
world_data = pd.concat([capitals, most_popular, least_popular]).drop_duplicates().reset_index(drop=True)

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
layer = pdk.Layer(
    "HeatMapLayer",
    data = world_data,
    get_position = ["longitude", "latitude"],
    color_range = COLOR_BREWER_BLUE_SCALE,
    get_weight = "temperature"
)
r = pdk.Deck(
    layers=layer,
    initial_view_state=pdk.data_utils.compute_view(capitals[['Longitude','Latitude']]),
    map_provider="mapbox",
)
r.to_html("heatmap_layer.html")

#Charts
fig1 = px.histogram(world_data,
                   x = "temperatureF",
                   title = "Most Common Heat World Wide (Farenheit)")
fig1.write_html('common_heat.html')
st.plotly_chart(fig1)

fig2 = px.histogram(world_data,
                   x = "temperatureC",
                   title = "Most Common Heat World Wide (Celsius)")
fig1.write_html('common_heat.html')
st.plotly_chart(fig1)

st.dataframe(world_data)