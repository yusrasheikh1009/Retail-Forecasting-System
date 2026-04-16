import numpy as np
from scipy.stats import norm

def advanced_inventory(
    forecast,
    current_stock,
    lead_time=7,
    service_level=0.95,
    ordering_cost=500,
    unit_cost=100,
    holding_rate=0.2
):

    forecast = np.array(forecast)

    # ======================
    # DEMAND DURING LEAD TIME
    # ======================
    mu_L = forecast[:lead_time].sum()

    # Estimate variability
    sigma_L = np.std(forecast) * np.sqrt(lead_time)

    # ======================
    # SAFETY STOCK
    # ======================
    z = norm.ppf(service_level)
    SS = z * sigma_L

    # ======================
    # REORDER POINT
    # ======================
    ROP = mu_L + SS

    # ======================
    # EOQ
    # ======================
    annual_demand = forecast.mean() * 365
    H = unit_cost * holding_rate

    EOQ = np.sqrt((2 * annual_demand * ordering_cost) / H) if H > 0 else mu_L

    # ======================
    # ORDER DECISION
    # ======================
    if current_stock < ROP:
        order_qty = max(EOQ, ROP - current_stock)
        status = "Reorder Required"
    else:
        order_qty = 0
        status = "Stock OK"

    return {
        "ROP": float(ROP),
        "SS": float(SS),
        "EOQ": float(EOQ),
        "order_qty": float(order_qty),
        "status": status
    }