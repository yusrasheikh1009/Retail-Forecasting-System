def promo_impact(df):

    promo_sales = df[df["on_promo"] == 1]["qty_sold"].mean()
    normal_sales = df[df["on_promo"] == 0]["qty_sold"].mean()

    uplift = ((promo_sales - normal_sales) / normal_sales) * 100

    return uplift