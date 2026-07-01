import streamlit as st

st.title("Weather Forecast for the Next Days")

place = st.text_input("Place:")
days = st.slider("Forecast Days:", min_value=1, max_value=5, help="Select the number of days for the weather forecast.")
option = st.selectbox("Data Type:", ["Temperature", "Sky"], help="Select the type of weather data you want to see.")
st.subheader(f"{option} for the next {days} days in {place}")