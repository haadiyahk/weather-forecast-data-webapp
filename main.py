import streamlit as st
import plotly.express as px
from backend import get_data

st.title("Weather Forecast for the Next Days")

place = st.text_input("Place:")
days = st.slider("Forecast Days:", min_value=1, max_value=5, help="Select the number of days for the weather forecast.")
option = st.selectbox("Data Type:", ["Temperature", "Sky"], help="Select the type of weather data you want to see.")
st.subheader(f"{option} for the next {days} days in {place}")

def get_data(days):
    dates = ["2024-06-01", "2024-06-02", "2024-06-03", "2024-06-04"]
    temperatures = [25, 27, 26, 28]
    temperatures = [days * i for i in temperatures]  # Simulate temperature changes based on the number of days
    return dates, temperatures

d, t = get_data(days)


figure = px.line(x=d, y=t, labels={"x": "Date", "y": "Temperature (°C)"})
st.plotly_chart(figure)