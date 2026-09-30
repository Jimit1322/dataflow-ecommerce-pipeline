import pandas as pd
from pathlib import Path


CLEAN_DIR = Path("data/processed/clean")


customers_df = pd.read_csv(
    CLEAN_DIR / "customers_clean.csv"
)

products_df = pd.read_csv(
    CLEAN_DIR / "products_clean.csv"
)

orders_df = pd.read_csv(
    CLEAN_DIR / "orders_clean.csv"
)


print("======================================")
print("       DATA QUALITY REPORT")
print("======================================")


print("\nCUSTOMERS")
print("Total records:", len(customers_df))
print(
    "Missing customer IDs:",
    customers_df["customer_id"].isna().sum()
)
print(
    "Duplicate customer IDs:",
    customers_df["customer_id"].duplicated().sum()
)


print("\nPRODUCTS")
print("Total records:", len(products_df))
print(
    "Missing product IDs:",
    products_df["product_id"].isna().sum()
)
print(
    "Invalid prices:",
    (products_df["price"] <= 0).sum()
)


print("\nORDERS")
print("Total records:", len(orders_df))
print(
    "Missing order IDs:",
    orders_df["order_id"].isna().sum()
)
print(
    "Duplicate order IDs:",
    orders_df["order_id"].duplicated().sum()
)
print(
    "Invalid quantities:",
    (orders_df["quantity"] <= 0).sum()
)
print(
    "Missing customer IDs:",
    orders_df["customer_id"].isna().sum()
)
print(
    "Missing product IDs:",
    orders_df["product_id"].isna().sum()
)


print("\n======================================")
print("       VALIDATION COMPLETED")
print("======================================")