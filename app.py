import streamlit as st
import pandas as pd
import numpy as np
import pickle

# 1. Load the model
model = pickle.load(open('ho_model.pkl', 'rb'))

# 2. Title for the app
st.title('House Price Prediction App')
st.write("Enter the property details to estimate the market price.")

# 3. Define inputs 
col1, col2 = st.columns(2)

with col1:
    sq_ft = st.number_input('Square Footage', min_value=500, max_value=10000, value=1500)
    bedrooms = st.number_input('Number of Bedrooms', min_value=1, max_value=10, value=3)
    bathrooms = st.number_input('Number of Bathrooms', min_value=1, max_value=8, value=2)
    year_built = st.number_input('Year Built', min_value=1800, max_value=2024, value=2000)

with col2:
    lot_size = st.number_input('Lot Size (sq ft)', min_value=1000, max_value=50000, value=5000)
    location = st.selectbox('Location Type', ('Urban', 'Suburban', 'Rural'))
    garage = st.selectbox('Garage Size (Cars)', (0, 1, 2, 3))
    condition = st.slider('House Condition (1-5)', 1, 5, 3)

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
if st.button('Estimate Price'):
    prediction = model.predict(input_df)
    
    formatted_price = f"${prediction[0]:,.2f}"
    
    st.success(f'Estimated Property Value: {formatted_price}')