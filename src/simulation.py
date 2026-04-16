import pandas as pd
import numpy as np
from src.inventory import advanced_inventory

def run_simulation(df, days=30):

    results = []

    # Initialize stock
    stock_levels = {}

    for (store, product), group in df.groupby(["store_id", "product_id"]):
        stock_levels[(store, product)] = np.random.randint(80, 150)

    # Run simulation day by day
    for day in range(days):

        daily_summary = []

        for (store, product), group in df.groupby(["store_id", "product_id"]):

            current_stock = stock_levels[(store, product)]

            # Simulate demand
            demand = max(0, int(np.random.normal(
                loc=group["qty_sold"].mean(),
                scale=5
            )))

            # Reduce stock
            current_stock -= demand

            # Prevent negative stock
            if current_stock < 0:
                current_stock = 0

            # Forecast (simple rolling mean)
            forecast = np.array([group["qty_sold"].mean()] * 7)

            # Inventory decision
            inv = advanced_inventory(forecast, current_stock)

            order_qty = int(inv["order_qty"])

            # If reorder → add stock
            if order_qty > 0:
                current_stock += order_qty

            # Save updated stock
            stock_levels[(store, product)] = current_stock

            daily_summary.append({
                "day": day,
                "store_id": store,
                "product_id": product,
                "demand": demand,
                "stock": current_stock,
                "order_qty": order_qty,
                "status": inv["status"]
            })

        results.extend(daily_summary)

    return pd.DataFrame(results)