import pandas as pd
import os

os.makedirs("outputs", exist_ok=True)

# Forecast data
forecast_df = pd.DataFrame({
    "product_id": [1, 2, 3],
    "forecast": [100, 150, 200],
    "recommended_stock": [110, 160, 210]
})

# Simulation data
sim_df = pd.DataFrame({
    "store_id": [1, 1, 2],
    "product_id": [1, 2, 3],
    "sales": [10, 20, 30]
})

forecast_df.to_csv("outputs/forecast_results.csv", index=False)
sim_df.to_csv("outputs/simulation_results.csv", index=False)

print("DONE: Files created")