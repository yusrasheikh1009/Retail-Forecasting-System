import pandas as pd
import numpy as np

def generate_data():
    np.random.seed(42)

    dates = pd.date_range(start="2022-01-01", end="2023-12-31")
    data = []

    for store in range(1, 4):
        for product in range(1, 6):
            demand = np.random.poisson(lam=20, size=len(dates))

            for i, date in enumerate(dates):
                data.append([
                    date,
                    store,
                    product,
                    max(0, demand[i] + np.random.randint(-5, 5))
                ])

    df = pd.DataFrame(data, columns=["date", "store_id", "product_id", "qty_sold"])

    df.to_csv("data/retail_data.csv", index=False)
    print("✅ Dataset generated at data/retail_data.csv")

if __name__ == "__main__":
    generate_data()