# import streamlit as st
# import numpy as np
# import pandas as pd
# import joblib
# from keras.models import load_model

# model = load_model("used_car_price_model.keras")
# scaler = joblib.load("scaler.pkl")

# st.set_page_config(page_title="Used Car Price Predictor", page_icon="🚗", layout="wide")

# st.markdown("""
# <style>
# body {
#     background: linear-gradient(135deg, #E3FDFD, #CBF1F5, #A6E3E9, #71C9CE);
#     background-attachment: fixed;
#     font-family: "Poppins", sans-serif;
# }
# h1, h2, h3 {
#     color: #003C43;
# }
# .stButton button {
#     background: linear-gradient(to right, #0072ff, #00c6ff);
#     color: white;
#     border-radius: 10px;
#     height: 3em;
#     width: 100%;
#     font-weight: 600;
#     font-size: 18px;
#     transition: 0.3s ease;
# }
# .stButton button:hover {
#     transform: scale(1.05);
#     background: linear-gradient(to right, #00c6ff, #0072ff);
# }
# .stSuccess {
#     background-color: #e8f5e9;
#     border-left: 5px solid #4CAF50;
#     border-radius: 10px;
#     padding: 15px;
#     font-size: 20px;
#     color: #2e7d32;
#     box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
# }
# .css-1d391kg, .css-12oz5g7 {
#     background-color: transparent !important;
# }
# .card {
#     background-color: white;
#     padding: 20px;
#     border-radius: 20px;
#     box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
# }
# footer {visibility: hidden;}
# </style>
# """, unsafe_allow_html=True)

# st.markdown("""
# <div style='text-align:center'>
#     <h1>🚗 Used Car Price Prediction</h1>
#     <h4>Get an instant estimate of your car’s resale value</h4>
#     <hr style='border:1px solid #0096c7; width:80%; margin:auto'>
# </div>
# <br>
# """, unsafe_allow_html=True)

# brand_model_map = {
#     'Maruti': ['Alto', 'Wagon R', 'Swift', 'Ciaz', 'Baleno', 'Vitara', 'Dzire VXI', 'S-Presso', 'Eeco', 'Ertiga', 'Ignis'],
#     'Hyundai': ['Grand', 'i10', 'i20', 'Creta', 'Verna', 'Venue', 'Elantra', 'Aura'],
#     'Ford': ['Ecosport', 'Figo', 'Aspire', 'Endeavour', 'Freestyle'],
#     'Renault': ['KWID', 'Triber', 'Duster'],
#     'Mini': ['Cooper'],
#     'Mercedes-Benz': ['C-Class', 'E-Class', 'GL-Class', 'GLS', 'S-Class'],
#     'Toyota': ['Innova', 'Fortuner', 'Camry', 'Yaris'],
#     'Volkswagen': ['Vento', 'Polo'],
#     'Honda': ['City', 'Amaze', 'Jazz', 'Civic', 'CR-V', 'WR-V'],
#     'Mahindra': ['Bolero', 'Scorpio', 'XUV500', 'Thar', 'KUV100', 'Marazzo', 'Alturas'],
#     'Tata': ['Tiago', 'Tigor', 'Safari', 'Harrier', 'Altroz', 'Nexon', 'Hexa'],
#     'Kia': ['Seltos', 'Carnival'],
#     'BMW': ['X1', 'X3', 'X4', 'X5', 'Z4', '7', '3', '5', '6'],
#     'Audi': ['A4', 'A6', 'A8'],
#     'Land Rover': ['Rover'],
#     'Jaguar': ['XF', 'XE', 'F-PACE'],
#     'MG': ['Hector'],
#     'ISUZU': ['D-Max', 'MUX'],
#     'Skoda': ['Rapid', 'Superb', 'Octavia'],
#     'Volvo': ['S90', 'XC', 'XC60', 'XC90'],
#     'Jeep': ['Compass', 'Wrangler'],
#     'Nissan': ['Kicks', 'GO'],
#     'Datsun': ['RediGO'],
#     'Maserati': ['Ghibli', 'Quattroporte'],
#     'Ferrari': ['GTC4Lusso'],
#     'Lexus': ['ES', 'NX', 'RX'],
#     'Porsche': ['Cayenne', 'Macan', 'Panamera'],
#     'Rolls-Royce': ['Ghost'],
#     'Force': ['Gurkha']
# }

# seller_types = ['Individual', 'Dealer', 'Trustmark Dealer']
# fuel_types = ['Petrol', 'Diesel', 'CNG', 'LPG', 'Electric']
# transmissions = ['Manual', 'Automatic']

# col1, col2, col3 = st.columns(3)
# with col1:
#     brand = st.selectbox("🏷️ Brand", sorted(brand_model_map.keys()))
# with col2:
#     filtered_models = brand_model_map.get(brand, [])
#     model_name = st.selectbox("🚘 Model", sorted(filtered_models))
# with col3:
#     seller_type = st.selectbox("🧾 Seller Type", seller_types)

# col4, col5, col6 = st.columns(3)
# with col4:
#     fuel_type = st.selectbox("⛽ Fuel Type", fuel_types)
# with col5:
#     transmission = st.selectbox("⚙️ Transmission", transmissions)
# with col6:
#     seats = st.number_input("💺 Seats", 2, 10, 5)

# col7, col8, col9 = st.columns(3)
# with col7:
#     vehicle_age = st.number_input("📅 Vehicle Age (years)", 0, 30, 5)
# with col8:
#     km_driven = st.number_input("📍 Kilometers Driven", 0, 400000, 40000)
# with col9:
#     mileage = st.number_input("🚦 Mileage (km/l)", 5.0, 50.0, 18.0)

# col10, col11 = st.columns(2)
# with col10:
#     engine = st.number_input("🔧 Engine (cc)", 600, 6000, 1200)
# with col11:
#     max_power = st.number_input("⚡ Max Power (bhp)", 30.0, 600.0, 80.0)

# def age_group(age):
#     if age <= 2:
#         return "new"
#     elif age > 2 and age <= 7:
#         return "mid"
#     elif age > 7 and age <= 12:
#         return "old"
#     else:
#         return "very_old"

# st.markdown("<br>", unsafe_allow_html=True)

# if st.button("🔮 Predict Car Price"):
#     age_grp = age_group(vehicle_age)
#     km_per_year = km_driven / (vehicle_age + 1)
#     power_per_litre = max_power / (engine / 1000)

#     input_data = {
#         "vehicle_age": vehicle_age,
#         "km_driven": km_driven,
#         "transmission_type": 0 if transmission == "Manual" else 1,
#         "mileage": mileage,
#         "engine": engine,
#         "max_power": max_power,
#         "seats": seats,
#         "km_per_year": km_per_year,
#         "power_per_litre": power_per_litre
#     }

#     df_input = pd.DataFrame([input_data])
#     df_input[f"brand_{brand}"] = 1
#     df_input[f"model_{model_name}"] = 1
#     df_input[f"seller_type_{seller_type}"] = 1
#     df_input[f"fuel_type_{fuel_type}"] = 1
#     df_input[f"age_group_{age_grp}"] = 1

#     expected_cols = scaler.feature_names_in_
#     for col in expected_cols:
#         if col not in df_input.columns:
#             df_input[col] = 0

#     df_input = df_input[expected_cols]
#     scaled_input = scaler.transform(df_input)
#     predicted_price = model.predict(scaled_input)[0][0]

#     st.markdown(f"""
#         <div class="card" style='text-align:center; background: linear-gradient(135deg, #e0f7fa, #b2ebf2);'>
#             <h2>💰 Predicted Selling Price</h2>
#             <h1 style='color:#00796b; font-size:45px;'>₹ {predicted_price:,.0f}</h1>
#             <p style='font-size:16px; color:#004d40;'>Based on your car’s features and performance</p>
#         </div>
#     """, unsafe_allow_html=True)

# else:
#     st.info("👆 Fill in the car details above and click **Predict Car Price** to see the result.")
