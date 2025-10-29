import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
import pandas as pd
import joblib
from keras.models import load_model
import json

app = FastAPI(title="Used Car Price Prediction API 🚗")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

model = None
scaler = None


def get_model_and_scaler():
    """Load ML model and scaler once for faster prediction."""
    global model, scaler
    if model is None or scaler is None:
        print("🔹 Loading model and scaler...")
        model = load_model("used_car_price_model.keras")
        scaler = joblib.load("scaler.pkl")
        print("✅ Model and scaler loaded successfully!")
    return model, scaler


brand_model_map = {
    'Maruti': ['Alto', 'Wagon R', 'Swift', 'Ciaz', 'Baleno', 'Vitara', 'Dzire VXI', 'S-Presso', 'Eeco', 'Ertiga', 'Ignis'],
    'Hyundai': ['Grand', 'i10', 'i20', 'Creta', 'Verna', 'Venue', 'Elantra', 'Aura'],
    'Ford': ['Ecosport', 'Figo', 'Aspire', 'Endeavour', 'Freestyle'],
    'Renault': ['KWID', 'Triber', 'Duster'],
    'Mini': ['Cooper'],
    'Mercedes-Benz': ['C-Class', 'E-Class', 'GL-Class', 'GLS', 'S-Class'],
    'Toyota': ['Innova', 'Fortuner', 'Camry', 'Yaris'],
    'Volkswagen': ['Vento', 'Polo'],
    'Honda': ['City', 'Amaze', 'Jazz', 'Civic', 'CR-V', 'WR-V'],
    'Mahindra': ['Bolero', 'Scorpio', 'XUV500', 'Thar', 'KUV100', 'Marazzo', 'Alturas'],
    'Tata': ['Tiago', 'Tigor', 'Safari', 'Harrier', 'Altroz', 'Nexon', 'Hexa'],
    'Kia': ['Seltos', 'Carnival'],
    'BMW': ['X1', 'X3', 'X4', 'X5', 'Z4', '7', '3', '5', '6'],
    'Audi': ['A4', 'A6', 'A8'],
    'Land Rover': ['Rover'],
    'Jaguar': ['XF', 'XE', 'F-PACE'],
    'MG': ['Hector'],
    'ISUZU': ['D-Max', 'MUX'],
    'Skoda': ['Rapid', 'Superb', 'Octavia'],
    'Volvo': ['S90', 'XC', 'XC60', 'XC90'],
    'Jeep': ['Compass', 'Wrangler'],
    'Nissan': ['Kicks', 'GO'],
    'Datsun': ['RediGO'],
    'Maserati': ['Ghibli', 'Quattroporte'],
    'Ferrari': ['GTC4Lusso'],
    'Lexus': ['ES', 'NX', 'RX'],
    'Porsche': ['Cayenne', 'Macan', 'Panamera'],
    'Rolls-Royce': ['Ghost'],
    'Force': ['Gurkha']
}

seller_types = ['Individual', 'Dealer', 'Trustmark Dealer']
fuel_types = ['Petrol', 'Diesel', 'CNG', 'LPG', 'Electric']
transmissions = ['Manual', 'Automatic']


def age_group(age: int):
    if age <= 2:
        return "new"
    elif age <= 7:
        return "mid"
    elif age <= 12:
        return "old"
    return "very_old"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main Home Page"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "brands": sorted(brand_model_map.keys()),
        "brand_model_map": json.dumps(brand_model_map),
        "seller_types": seller_types,
        "fuel_types": fuel_types,
        "transmissions": transmissions
    })


@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    brand: str = Form(...),
    model_name: str = Form(...),
    seller_type: str = Form(...),
    fuel_type: str = Form(...),
    transmission: str = Form(...),
    seats: int = Form(...),
    vehicle_age: int = Form(...),
    km_driven: int = Form(...),
    mileage: float = Form(...),
    engine: int = Form(...),
    max_power: float = Form(...)
):
    """Handle prediction request."""
    model, scaler = get_model_and_scaler()

    age_grp = age_group(vehicle_age)
    km_per_year = km_driven / (vehicle_age + 1)
    power_per_litre = max_power / (engine / 1000)

    input_data = {
        "vehicle_age": vehicle_age,
        "km_driven": km_driven,
        "transmission_type": 0 if transmission == "Manual" else 1,
        "mileage": mileage,
        "engine": engine,
        "max_power": max_power,
        "seats": seats,
        "km_per_year": km_per_year,
        "power_per_litre": power_per_litre
    }

    df_input = pd.DataFrame([input_data])
    df_input[f"brand_{brand}"] = 1
    df_input[f"model_{model_name}"] = 1
    df_input[f"seller_type_{seller_type}"] = 1
    df_input[f"fuel_type_{fuel_type}"] = 1
    df_input[f"age_group_{age_grp}"] = 1

    all_columns = list(scaler.feature_names_in_)
    missing_cols = [col for col in all_columns if col not in df_input.columns]
    if missing_cols:
        zeros_df = pd.DataFrame(0, index=df_input.index, columns=missing_cols)
        df_input = pd.concat([df_input, zeros_df], axis=1)
    df_input = df_input[all_columns].copy()

    scaled_input = scaler.transform(df_input)
    predicted_price = float(model.predict(scaled_input)[0][0])

    form_data = {
        "brand": brand,
        "model_name": model_name,
        "seller_type": seller_type,
        "fuel_type": fuel_type,
        "transmission": transmission,
        "seats": seats,
        "vehicle_age": vehicle_age,
        "km_driven": km_driven,
        "mileage": mileage,
        "engine": engine,
        "max_power": max_power
    }

    return templates.TemplateResponse("index.html", {
        "request": request,
        "brands": sorted(brand_model_map.keys()),
        "brand_model_map": json.dumps(brand_model_map),
        "seller_types": seller_types,
        "fuel_types": fuel_types,
        "transmissions": transmissions,
        "predicted_price": f"₹ {predicted_price:,.0f}",
        "form_data": json.dumps(form_data)
    })
