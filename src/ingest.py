import pandas as pd
import json
from pathlib import Path


# --------------------------------
# Configuration
# --------------------------------

RAW_DIR = Path("data/raw")


# --------------------------------
# Load customers
# --------------------------------

with open(RAW_DIR / "customers.json", "r") as file:
    customers_data = json.load(file)

customers_df = pd.DataFrame(customers_data)

def check_columns(df, required_columns, dataset_name):
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{dataset_name} is missing columns: {missing_columns}"
        )

    print(f"{dataset_name}: schema check passed.")



# --------------------------------
# Load products
# --------------------------------

products_df = pd.read_csv(
    RAW_DIR / "products.csv"
)


# --------------------------------
# Load orders
# --------------------------------

orders_df = pd.read_csv(
    RAW_DIR / "orders.csv"
)

check_columns(
    customers_df,
    ["customer_id", "name", "city", "email"],
    "Customers"
)

check_columns(
    products_df,
    ["product_id", "product_name", "category", "price"],
    "Products"
)

check_columns(
    orders_df,
    ["order_id", "customer_id", "product_id", "quantity", "order_date"],
    "Orders"
)

# --------------------------------
# Display information
# --------------------------------

print("\n========== CUSTOMERS ==========")

print("Rows:", len(customers_df))
print("Columns:", list(customers_df.columns))

print("\nSample:")
print(customers_df.head())


print("\n========== PRODUCTS ==========")

print("Rows:", len(products_df))
print("Columns:", list(products_df.columns))

print("\nSample:")
print(products_df.head())


print("\n========== ORDERS ==========")

print("Rows:", len(orders_df))
print("Columns:", list(orders_df.columns))

print("\nSample:")
print(orders_df.head())

print("\n========== DATA TYPES ==========")

print("\nCustomers:")
print(customers_df.dtypes)

print("\nProducts:")
print(products_df.dtypes)

print("\nOrders:")
print(orders_df.dtypes)

PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

customers_df.to_csv(
    PROCESSED_DIR / "customers_ingested.csv",
    index=False
)

products_df.to_csv(
    PROCESSED_DIR / "products_ingested.csv",
    index=False
)

orders_df.to_csv(
    PROCESSED_DIR / "orders_ingested.csv",
    index=False
)

print("\nIngestion completed successfully.")