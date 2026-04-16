import numpy as np
from sklearn.ensemble import RandomForestRegressor

# ======================
# TRAIN MODEL
# ======================
def train_model(X, y):
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X, y)
    return model

# ======================
# FORECAST FUNCTION (FIX)
# ======================
def forecast_demand(model, X):
    predictions = model.predict(X)

    # Ensure no negative demand
    predictions = np.maximum(0, predictions)

    return predictions