from fastapi import FastAPI
import pandas as pd
import numpy as np

from src.data_preprocessing import load_data
from src.feature_engineering import create_features
from src.model import train_model
from src.inventory import advanced_inventory

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Retail Inventory API Running 🚀"}


@app.post("/predict")
def predict(store_id: int, product_id: int):

    # Load data
    df = load_data()

    # Filter SKU
    df = df[(df["store_id"] == store_id) & (df["product_id"] == product_id)]

    if len(df) < 30:
        return {"error": "Not enough data for this SKU"}

    # Feature engineering
    df = create_features(df)

    X = df[["lag_1", "lag_7", "rolling_mean", "day_of_week", "on_promo"]]
    y = df["qty_sold"]

    # Train model
    model = train_model(X, y)

    # Forecast
    preds = model.predict(X)
    forecast = preds[-7:]

    # Simulate stock
    current_stock = int(np.random.randint(50, 200))

    # Inventory decision
    result = advanced_inventory(forecast, current_stock)

    return {
        "store_id": store_id,
        "product_id": product_id,
        "forecast_next_7_days": forecast.tolist(),
        "current_stock": current_stock,
        "reorder_point": result["reorder_point"],
        "safety_stock": result["safety_stock"],
        "EOQ": result["EOQ"],
        "order_quantity": result["order_qty"],
        "status": result["status"]
    }