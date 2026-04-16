import streamlit as st
import pandas as pd
import numpy as np

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Retail Intelligence AI",
    layout="wide",
    page_icon="📊"
)

# =========================
# HEADER
# =========================
st.title("📊 Retail Intelligence AI Dashboard")
st.markdown("Forecasting • Inventory Optimization • Simulation Engine")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    try:
        forecast_df = pd.read_csv("outputs/forecast_results.csv")
        sim_df = pd.read_csv("outputs/simulation_results.csv")
        return forecast_df, sim_df
    except:
        st.error("❌ Missing CSV files. Run data generation first.")
        return pd.DataFrame(), pd.DataFrame()

forecast_df, sim_df = load_data()

if forecast_df.empty or sim_df.empty:
    st.stop()

# =========================
# SIDEBAR NAVIGATION
# =========================
page = st.sidebar.radio(
    "📌 Navigation",
    ["📈 Forecast Dashboard", "📦 Inventory Planner", "🔄 Simulation Engine"]
)

# =========================
# 📈 FORECAST DASHBOARD
# =========================
if page == "📈 Forecast Dashboard":

    st.subheader("Demand Forecast Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Products", forecast_df["product_id"].nunique())
    col2.metric("Avg Forecast", round(forecast_df["forecast"].mean(), 2))
    col3.metric("Max Forecast", forecast_df["forecast"].max())

    st.divider()

    st.dataframe(forecast_df, use_container_width=True)

    st.line_chart(forecast_df.set_index("product_id")["forecast"])

    csv = forecast_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Forecast Data", csv, "forecast.csv", "text/csv")

# =========================
# 📦 INVENTORY PLANNER (SPLIT VIEW)
# =========================
elif page == "📦 Inventory Planner":

    st.subheader("Smart Inventory Recommendations")

    df = forecast_df.copy()

    # =========================
    # RESTOCK LOGIC
    # =========================
    df["restock_status"] = np.where(
        df["recommended_stock"] > df["forecast"],
        "🟢 Restock Required",
        "🔴 Not Required"
    )

    # =========================
    # METRICS
    # =========================
    col1, col2 = st.columns(2)

    col1.metric("Total Products", len(df))
    col2.metric("Restock Needed", (df["restock_status"] == "🟢 Restock Required").sum())

    st.divider()

    # =========================
    # SPLIT TABLES
    # =========================

    restock_df = df[df["restock_status"] == "🟢 Restock Required"]
    no_restock_df = df[df["restock_status"] == "🔴 Not Required"]

    st.subheader("🟢 Restock Required Products")
    st.dataframe(restock_df, use_container_width=True)

    st.subheader("🔴 No Restock Needed Products")
    st.dataframe(no_restock_df, use_container_width=True)

    st.divider()

    st.bar_chart(df.set_index("product_id")["recommended_stock"])

# =========================
# 🔄 SIMULATION ENGINE
# =========================
elif page == "🔄 Simulation Engine":

    st.subheader("Retail Stock Movement Simulation")

    store_map = {1: "Store A", 2: "Store B", 3: "Store C"}
    product_map = {1: "Laptop", 2: "Mobile", 3: "Headphones", 4: "TV", 5: "Shoes"}

    sim_df["store_name"] = sim_df["store_id"].map(store_map)
    sim_df["product_name"] = sim_df["product_id"].map(product_map)

    col1, col2 = st.columns(2)

    store = col1.selectbox("Select Store", sim_df["store_name"].dropna().unique())
    product = col2.selectbox("Select Product", sim_df["product_name"].dropna().unique())

    filtered = sim_df[
        (sim_df["store_name"] == store) &
        (sim_df["product_name"] == product)
    ]

    st.divider()

    if filtered.empty:
        st.warning("No data found for selection")
    else:
        st.dataframe(filtered, use_container_width=True)

        if "sales" in filtered.columns:
            st.line_chart(filtered["sales"])