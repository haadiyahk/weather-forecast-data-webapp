import streamlit as st
import plotly.express as px
from backend import get_data, get_current_weather

st.set_page_config(
    page_title="Weather Forecast Dashboard",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌤️ Weather Forecast Dashboard")
st.write("Get an interactive weather forecast for any city.")

#INPUTS
forecast_options = {
    "Today": 0,
    "Next 1 Day": 1,
    "Next 2 Days": 2,
    "Next 3 Days": 3,
    "Next 4 Days": 4,
    "Next 5 Days": 5,
}

col1, col2 = st.columns(2)
with col1:
    place = st.text_input("City:")

with col2:
    forecast_option = st.selectbox(
        "Forecast Period",
        list(forecast_options.keys())
    )

    days = forecast_options[forecast_option]

option = st.selectbox(
    "📊 Data Type",
    [
        "Temperature",
        "Humidity",
        "Pressure",
        "Wind Speed"
    ],
    help="Select the type of weather data you want to see."
)

search = st.button("🔍 Get Forecast")

# OUTPUT
if search:
    if not place:
        st.warning("Please enter a city name.")
    else:
        try:
            with st.spinner("Fetching weather data..."):
                current = get_current_weather(place)
                filtered_data= get_data(place, days)
            
# CURRENT WEATHER CARD
            st.subheader(f"📍 {current['name']}")

            st.write(
                f"**{current['weather'][0]['description'].title()}**"
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("🌡 Temperature", f"{current['main']['temp']:.1f}°C")
                # :.1f means upto 1 decimal place
            
            with col2:
                st.metric("Feels Like", f"{current['main']['feels_like']:.1f}°C")

            with col3:
                st.metric("💧 Humidity", f"{current['main']['humidity']}%")

            with col4:
                st.metric("💨 Wind Speed", f"{current['wind']['speed']} m/s")

            st.divider()

#GRAPH CODE
            dates = [
                item["dt_txt"]
                for item in filtered_data
            ]  #dt_data is the list of dates in the filtered_data(debug)

            weather_data = {

                "Temperature": {
                    "values": [
                        item["main"]["temp"]
                        for item in filtered_data
                    ],
                    "ylabel": "Temperature (°C)"
                },

                "Humidity": {
                    "values": [
                        item["main"]["humidity"]
                        for item in filtered_data
                    ],
                    "ylabel": "Humidity (%)"
                },

                "Pressure": {
                    "values": [
                        item["main"]["pressure"]
                        for item in filtered_data
                    ],
                    "ylabel": "Pressure (hPa)"
                },

                "Wind Speed": {
                    "values": [
                        item["wind"]["speed"]
                        for item in filtered_data
                    ],
                    "ylabel": "Wind Speed (m/s)"
                }

            }

            values = weather_data[option]["values"]
            ylabel = weather_data[option]["ylabel"]

            st.subheader(f"{option} • {forecast_option}")

            figure = px.line(
                x=dates,
                y=values,
                labels={
                    "x": "Date & Time",
                    "y": ylabel
                }
            )

            figure.update_traces(
                mode="lines+markers"
            )

            figure.update_layout(
                hovermode="x unified"
            )

            st.plotly_chart(
                figure,
                use_container_width=True
            )

        except KeyError:
            st.write("That place does not exist.")