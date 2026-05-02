import streamlit as st
import numpy as np
import joblib
import os

# Load the model with error handling
model_file = 'solar_model.pkl'  # Path to the model file
if os.path.exists(model_file):
    try:
        model = joblib.load(model_file)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()
else:
    st.error(f"Model file '{model_file}' not found. Please upload it.")
    st.stop()

# Set the page layout for optimal use of space
st.set_page_config(page_title="Solar Power Prediction", page_icon="☀️", layout="wide")

# Centered Title and Description
st.markdown("<h1 style='text-align: center;'>🌞 Solar Power Prediction App</h1>", unsafe_allow_html=True)
st.markdown("""
    <p style='text-align: center;'>
        Predict solar power output (in kW) based on weather and environmental features.<br>
        Adjust the inputs below and see real-time predictions.
    </p>
""", unsafe_allow_html=True)

# Gap between the header and columns
st.markdown("<br><br>", unsafe_allow_html=True)

# Columns for better layout and fitting
col1, col2, col3 = st.columns([1, 1, 1])  # Equal width for all columns

# Column 1: General Features (Collapsible with updated emoji 🌞)
with col1:
    with st.expander("☀️ General Features"):
        distance_to_solar_noon = st.slider("Distance to Solar Noon (hours)", 0.0, 6.0, 1.5, step=0.05)
        temperature = st.slider("Temperature (°C)", -10.0, 50.0, 25.0, step=0.05)
        solar_intensity_factor = st.slider("Solar Intensity Factor", 0.0, 1.0, 0.9)
        sky_cover = st.slider("Sky Cover (scale 0-1)", 0.0, 1.0, 0.2)

# Column 2: Wind Features (Collapsible)
with col2:
    with st.expander("💨 Wind Features"):
        wind_speed = st.slider("Wind Speed (m/s)", 0.0, 15.0, 3.0)
        wind_direction = st.slider("Wind Direction (degrees)", 0, 360, 90)
        wind_u = st.slider("Wind U Component (m/s)", -5.0, 5.0, 1.0)
        wind_v = st.slider("Wind V Component (m/s)", -5.0, 5.0, -0.5)
        average_wind_speed = st.slider("Average Wind Speed (m/s)", 0.0, 15.0, 2.8)

# Column 3: Advanced Features (Collapsible)
with col3:
    with st.expander("📊 Advanced Features"):
        average_pressure = st.slider("Average Pressure (hPa)", 950, 1050, 1012)
        humidity = st.slider("Humidity (%)", 0, 100, 40)
        temp_humidity_interaction = st.slider("Temp-Humidity Interaction", 0.0, 50.0, 10.0)




# Adding the prediction button
if st.button("✨ Predict Solar Power"):
    # Prepare the features for prediction
    features = np.array([[ 
        distance_to_solar_noon, temperature, solar_intensity_factor, sky_cover, 
        wind_speed, wind_direction, wind_u, wind_v, average_wind_speed, 
        average_pressure, humidity, temp_humidity_interaction 
    ]])
    
    # Prediction
    try:
        prediction = model.predict(features)
        st.success(f"🌟 Predicted Solar Power Output: **{prediction[0]:.2f} kW**")
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")