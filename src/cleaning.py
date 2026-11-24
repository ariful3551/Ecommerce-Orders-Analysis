"""Cleaning script for the e-commerce orders dataset (beginner-friendly version).

It repeats the steps of notebooks/02_data_cleaning.ipynb in the same order.
The reason for every step is written in docs/cleaning_decisions.md.

How to run (from the project root folder):
    python src/cleaning.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

# Folder of the project (one level above the "src" folder)
ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "data" / "raw" / "ecommerce_orders_raw.csv"
CLEAN_PATH = ROOT / "data" / "processed" / "ecommerce_orders_clean.csv"

# Dictionaries that map every spelling (written in lowercase) to one standard name
GENDER_MAP = {
    "f": "Female", "female": "Female", "woman": "Female",
    "m": "Male", "male": "Male",
}

COUNTRY_MAP = {
    "germany": "Germany", "deutschland": "Germany", "de": "Germany",
    "france": "France", "fr": "France",
    "austria": "Austria", "österreich": "Austria", "at": "Austria",
    "netherlands": "Netherlands", "the netherlands": "Netherlands", "nl": "Netherlands",
    "switzerland": "Switzerland", "schweiz": "Switzerland", "ch": "Switzerland",
    "belgium": "Belgium", "be": "Belgium",
}

CATEGORY_MAP = {
    "electronics": "Electronics", "electronic": "Electronics", "elec": "Electronics",
    "fashion": "Fashion",
    "home & kitchen": "Home & Kitchen", "home and kitchen": "Home & Kitchen",
    "home_kitchen": "Home & Kitchen",
    "office": "Office",
    "sports": "Sports", "sport": "Sports",
}


def clean_orders(raw):
    """Take the raw table and return the cleaned table."""

    # Work on a copy so the raw data is never changed
    df = raw.copy()

    # Step 1: remove extra spaces from every text column
    for col in df.select_dtypes(exclude="number").columns:
        df[col] = df[col].str.strip()

    # Step 2: Order_Date is text in three formats, so parse each format and combine them
    iso = pd.to_datetime(df["Order_Date"], format="%Y-%m-%d", errors="coerce")    # 2024-05-27
    dmy = pd.to_datetime(df["Order_Date"], format="%d/%m/%Y", errors="coerce")    # 27/05/2024
    mon = pd.to_datetime(df["Order_Date"], format="%b %d, %Y", errors="coerce")   # May 27, 2024
    df["Order_Date"] = iso.fillna(dmy).fillna(mon)

    # Step 3: make the spellings of Gender, Country and Category consistent
    df["Gender"] = df["Gender"].str.lower().map(GENDER_MAP)
    df["Country"] = df["Country"].str.lower().map(COUNTRY_MAP)
    df["Category"] = df["Category"].str.lower().map(CATEGORY_MAP)

    # Step 4: remove exact duplicate rows
    df = df.drop_duplicates()

    # Step 5: fix Quantity <= 0 using Profit = Sales - Quantity x Cost
    # so Quantity = (Sales - Profit) / Cost
    bad_quantity = df["Quantity"] <= 0
    quantity_from_formula = ((df["Sales"] - df["Profit"]) / df["Cost"]).round()
    df.loc[bad_quantity, "Quantity"] = quantity_from_formula[bad_quantity].astype("int64")

    # Step 6: impossible values cannot be trusted, so set them to missing (NaN)
    df.loc[~df["Age"].between(16, 90), "Age"] = np.nan
    df.loc[~df["Discount"].between(0, 0.9), "Discount"] = np.nan
    df.loc[~df["Customer_Rating"].between(1, 5), "Customer_Rating"] = np.nan
    df.loc[df["Delivery_Days"] < 0, "Delivery_Days"] = np.nan

    # Step 7: fill missing Discount using Sales = Quantity x Unit_Price x (1 - Discount)
    # so Discount = 1 - Sales / (Quantity x Unit_Price)
    missing_discount = df["Discount"].isna()
    discount_from_formula = (1 - df["Sales"] / (df["Quantity"] * df["Unit_Price"])).round(3)
    df.loc[missing_discount, "Discount"] = discount_from_formula[missing_discount]

    # Step 8: fill missing City from Region, but only when the region has exactly one city
    region_to_city = {}
    for region, group in df.groupby("Region"):
        cities = group["City"].dropna().unique()
        if len(cities) == 1:
            region_to_city[region] = cities[0]
    df["City"] = df["City"].fillna(df["Region"].map(region_to_city))

    # Step 9: columns that cannot be recovered are filled with "Unknown"
    unknown_columns = [
        "Customer_Name", "Gender", "Customer_Segment",
        "Payment_Method", "Marketing_Channel", "City",
    ]
    for col in unknown_columns:
        df[col] = df[col].fillna("Unknown")

    # Step 10: a cancelled order has no delivery and no rating
    cancelled = df["Order_Status"] == "Cancelled"
    df.loc[cancelled, ["Customer_Rating", "Delivery_Days"]] = np.nan

    # Step 11: whole-number columns that can contain missing values
    df["Age"] = df["Age"].astype("Int64")
    df["Delivery_Days"] = df["Delivery_Days"].astype("Int64")

    # Step 12: new columns (Cost is a cost per unit, so total cost = Quantity x Cost)
    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.month
    df["Total_Cost"] = (df["Quantity"] * df["Cost"]).round(2)

    # Step 13: final checks. If a rule is broken, the script stops with an error.
    assert df["Order_ID"].is_unique
    assert df["Order_Date"].notna().all()
    assert df["Gender"].isin(["Male", "Female", "Unknown"]).all()
    assert df["Country"].nunique() == 6
    assert df["Category"].nunique() == 5
    assert df["Quantity"].between(1, 5).all()
    assert df["Discount"].between(0, 0.9).all()
    assert df["Customer_Rating"].dropna().between(1, 5).all()
    assert (df["Delivery_Days"].dropna() >= 0).all()
    assert df["Age"].dropna().between(16, 90).all()
    assert ((df["Profit"] - (df["Sales"] - df["Total_Cost"])).abs() < 0.05).all()
    assert (df["Returned"] == (df["Order_Status"] == "Returned").astype(int)).all()

    return df


def main():
    raw = pd.read_csv(RAW_PATH)
    clean = clean_orders(raw)

    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(CLEAN_PATH, index=False)

    print("Raw rows and columns:  ", raw.shape)
    print("Clean rows and columns:", clean.shape)
    print("All checks passed. Saved to", CLEAN_PATH)


if __name__ == "__main__":
    main()