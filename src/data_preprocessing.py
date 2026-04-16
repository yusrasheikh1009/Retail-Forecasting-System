import pandas as pd
import numpy as np

def load_data():
    df = pd.read_csv("data/retail_data.csv", parse_dates=["date"])

    # ======================
    # FIX: ADD PROMO COLUMN
    # ======================
    if "on_promo" not in df.columns:
        df["on_promo"] = np.random.choice([0, 1], size=len(df), p=[0.8, 0.2])

    # ======================
    # SIMULATE PROMO IMPACT
    # ======================
    df["qty_sold"] = df["qty_sold"] * (1 + df["on_promo"] * np.random.uniform(0.2, 0.5))

    return df