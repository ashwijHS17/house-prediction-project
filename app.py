import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>

.main {
    background: linear-gradient(120deg,#1d4350,#a43931);
}

h1, h2, h3, h4 {
    color: white !important;
}

label, .stSelectbox label, .stNumberInput label {
    color: white !important;
}

.stNumberInput input {
    background-color: #f0f2f6 !important;
    color: black !important;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #f0f2f6 !important;
    color: black !important;
}

.stSlider > div {
    color: white !important;
}

.stButton>button {
    background: linear-gradient(90deg,#11998e,#38ef7d);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
}

.card {
    background-color: rgba(255,255,255,0.1);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}

.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# 1. Load the model
model = pickle.load(open('ho_model.pkl', 'rb'))

# ---------- TITLE ----------
st.markdown("<h1 style='text-align:center;'>🏠 House Price Prediction Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Enter property details to estimate the market value</h4>", unsafe_allow_html=True)
st.write("")

# 2. Define inputs 
st.markdown("<div class='card'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📐 Property Details")
    sq_ft = st.number_input('Square Footage', min_value=500, max_value=10000, value=1500)
    bedrooms = st.number_input('Number of Bedrooms', min_value=1, max_value=10, value=3)
    bathrooms = st.number_input('Number of Bathrooms', min_value=1, max_value=8, value=2)
    year_built = st.number_input('Year Built', min_value=1800, max_value=2024, value=2000)

with col2:
    st.subheader("📍 Extra Features")
    lot_size = st.number_input('Lot Size (sq ft)', min_value=1000, max_value=50000, value=5000)
    location = st.selectbox('Location Type', ('Urban', 'Suburban', 'Rural'))
    garage = st.selectbox('Garage Size (Cars)', (0, 1, 2, 3))
    condition = st.slider('House Condition (1-5)', 1, 5, 3)

st.markdown("</div>", unsafe_allow_html=True)
st.write("")

# 4. Encoding & Preprocessing
def preprocess_input():
    location_map = {'Rural': 0, 'Suburban': 1, 'Urban': 2}
    
    data = {
        'Square_Footage': sq_ft,
        'Num_Bedrooms': bedrooms,
        'Num_Bathrooms': bathrooms,
        'Lot_Size': lot_size,
        'Year_Built': year_built,
        'Garage_Size': garage,
        'Neighborhood_Quality': condition, 
        'Location_Score': location_map[location]
    }
    return pd.DataFrame([data])

input_df = preprocess_input()

# 5. Predictions
if st.button('💰 Estimate Price'):
    prediction = model.predict(input_df)
    
    formatted_price = f"${prediction[0]:,.2f}"
    
    st.markdown(f"""
    <div style='background:#00c853;padding:25px;border-radius:15px;text-align:center'>
        <h2 style='color:white;'>Estimated Property Value</h2>
        <h1 style='color:white;'>{formatted_price}</h1>
    </div>
    """, unsafe_allow_html=True)
