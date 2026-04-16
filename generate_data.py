import pandas as pd
import numpy as np
import os

os.makedirs("outputs", exist_ok=True)

# =========================
# CONFIG
# =========================
np.random.seed(42)

stores = [1, 2, 3, 4, 5]
products = list(range(1, 21))  # 20 products

# =========================
# FORECAST DATA (100+ rows)
# =========================
forecast_data = []

for p in products:
    forecast = np.random.randint(50, 300)
    recommended = forecast + np.random.randint(10, 50)

    forecast_data.append([p, forecast, recommended])

forecast_df = pd.DataFrame(forecast_data, columns=[
    "product_id", "forecast", "recommended_stock"
])

# =========================
# SIMULATION DATA (100+ rows)
# =========================
sim_data = []

for s in stores:
    for p in products:
        for day in range(1, 6):  # 5 days simulation
            sales = np.random.randint(5, 50)
            stock = np.random.randint(50, 200)

            sim_data.append([s, p, day, sales, stock])

sim_df = pd.DataFrame(sim_data, columns=[
    "store_id", "product_id", "day", "sales", "stock"
])

# =========================
# SAVE FILES
# =========================
forecast_df.to_csv("outputs/forecast_results.csv", index=False)
sim_df.to_csv("outputs/simulation_results.csv", index=False)

print("✅ Large dataset created successfully!")