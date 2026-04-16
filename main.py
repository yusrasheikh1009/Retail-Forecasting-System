import pandas as pd
import numpy as np

from src.data_preprocessing import load_data
from src.feature_engineering import create_features
from src.model import train_model, forecast_demand
from src.inventory import advanced_inventory
from src.model_compare import compare_models
from src.anomaly import detect_anomalies
from src.promo_analysis import promo_impact
from src.simulation import run_simulation

# ======================
# LOAD DATA
# ======================
print("📥 Loading data...")
df = load_data()

# ======================
# FEATURE ENGINEERING
# ======================
print("⚙️ Creating features...")
df = create_features(df)

# Drop NA values from lag features
df = df.dropna()

# ======================
# PREPARE TRAINING DATA
# ======================
features = [col for col in df.columns if col not in ["qty_sold", "date"]]

X = df[features]
y = df["qty_sold"]

# ======================
# MODEL TRAINING
# ======================
print("🤖 Training model...")
model = train_model(X, y)

# ======================
# FORECASTING
# ======================
print("🔮 Generating forecast...")
forecast = forecast_demand(model, X)

# ======================
# INVENTORY OPTIMIZATION
# ======================
print("📦 Running inventory optimization...")

inventory_results = []

for i in range(len(df)):

    current_stock = np.random.randint(50, 150)

    # 7-day forecast slice
    forecast_slice = forecast[i:i+7] if i+7 < len(forecast) else forecast[i:]

    inv = advanced_inventory(
        forecast=np.array(forecast_slice),
        current_stock=current_stock
    )

    inventory_results.append({
        "store_id": df.iloc[i]["store_id"],
        "product_id": df.iloc[i]["product_id"],
        "forecast": int(np.mean(forecast_slice)),
        "current_stock": current_stock,
        "reorder_point": inv["ROP"],
        "safety_stock": inv["SS"],
        "EOQ": inv["EOQ"],
        "order_qty": inv["order_qty"],
        "status": inv["status"]
    })

inventory_df = pd.DataFrame(inventory_results)

# ======================
# SAVE OUTPUT
# ======================
inventory_df.to_csv("outputs/inventory_recommendations.csv", index=False)

print("\n📊 INVENTORY OPTIMIZATION REPORT\n")
print(inventory_df.head())

# ======================
# MODEL COMPARISON
# ======================
print("\n📊 MODEL COMPARISON:")
comparison = compare_models(X, y)
print(comparison)

# ======================
# ANOMALY DETECTION
# ======================
anomalies = detect_anomalies(df)
print(f"\n🚨 Anomalies Detected: {len(anomalies)}")

# ======================
# PROMOTION IMPACT
# ======================
uplift = promo_impact(df)
print(f"\n💰 Promotion Sales Uplift: {round(uplift,2)}%")

# ======================
# SIMULATION ENGINE (🔥 IMPORTANT)
# ======================
print("\n🔄 Running Retail Simulation...")

sim_df = run_simulation(df, days=30)

sim_df.to_csv("outputs/simulation_results.csv", index=False)

print("✅ Simulation completed")
print("📁 Saved: outputs/simulation_results.csv")

# ======================
# FINAL MESSAGE
# ======================
print("\n✅ PROJECT EXECUTION COMPLETED SUCCESSFULLY 🚀")
print("📁 Check outputs/ folder for results")