from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

def compare_models(X, y):

    models = {
        "RandomForest": RandomForestRegressor(),
        "LinearRegression": LinearRegression()
    }

    results = {}

    for name, model in models.items():
        model.fit(X, y)
        pred = model.predict(X)
        mae = mean_absolute_error(y, pred)
        results[name] = round(mae, 2)

    return results