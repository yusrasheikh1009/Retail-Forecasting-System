def create_features(df):
    df = df.sort_values("date")

    df["lag_1"] = df["qty_sold"].shift(1)
    df["lag_7"] = df["qty_sold"].shift(7)

    df["rolling_mean"] = df["qty_sold"].shift(1).rolling(7).mean()

    df = df.dropna()
    return df