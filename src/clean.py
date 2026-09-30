import pandas as pd
from pathlib import Path


# --------------------------------
# Configuration
# --------------------------------

PROCESSED_DIR = Path("data/processed")


# --------------------------------
# Load ingested data
# --------------------------------

customers_df = pd.read_csv(
    PROCESSED_DIR / "customers_ingested.csv"
)

products_df = pd.read_csv(
    PROCESSED_DIR / "products_ingested.csv"
)

orders_df = pd.read_csv(
    PROCESSED_DIR / "orders_ingested.csv"
)


print("Data loaded successfully.")


# --------------------------------
# Basic information
# --------------------------------

print("\nCustomers:")
print(customers_df.info())

print("\nProducts:")
print(products_df.info())

print("\nOrders:")
print(orders_df.info())

print("\n========== MISSING VALUES ==========")

print("\nCustomers:")
print(customers_df.isnull().sum())

print("\nProducts:")
print(products_df.isnull().sum())

print("\nOrders:")
print(orders_df.isnull().sum())

print("\n========== DUPLICATES ==========")

print(
    "Duplicate customers:",
    customers_df.duplicated().sum()
)

print(
    "Duplicate products:",
    products_df.duplicated().sum()
)

print(
    "Duplicate orders:",
    orders_df.duplicated().sum()
)

duplicate_order_ids = (
    orders_df["order_id"].duplicated().sum()
)

print(
    "Duplicate order IDs:",
    duplicate_order_ids
)

invalid_quantity = orders_df[
    orders_df["quantity"] <= 0
]

print(
    "Invalid quantity records:",
    len(invalid_quantity)
)

invalid_price = products_df[
    products_df["price"] <= 0
]

print(
    "Invalid price records:",
    len(invalid_price)
)

orders_df["order_date"] = pd.to_datetime(
    orders_df["order_date"],
    errors="coerce"
)
invalid_dates = orders_df[
    orders_df["order_date"].isna()
]

print(
    "Invalid dates:",
    len(invalid_dates)
)

orders_df = orders_df.merge(
    products_df[
        ["product_id", "price"]
    ],
    on="product_id",
    how="left"
)
orders_df["total_amount"] = (
    orders_df["quantity"] *
    orders_df["price"]
)


# Remove duplicate orders
orders_df = orders_df.drop_duplicates(
    subset=["order_id"]
)


# Remove invalid quantities
orders_df = orders_df[
    orders_df["quantity"] > 0
]


# Remove invalid prices
products_df = products_df[
    products_df["price"] > 0
]


# Remove orders with missing essential fields
orders_df = orders_df.dropna(
    subset=[
        "order_id",
        "customer_id",
        "product_id",
        "order_date"
    ]
)

CLEAN_DIR = Path("data/processed/clean")

CLEAN_DIR.mkdir(
    parents=True,
    exist_ok=True
)
customers_df.to_csv(
    CLEAN_DIR / "customers_clean.csv",
    index=False
)

products_df.to_csv(
    CLEAN_DIR / "products_clean.csv",
    index=False
)

orders_df.to_csv(
    CLEAN_DIR / "orders_clean.csv",
    index=False
)

print("\nCleaning completed successfully.")

print("Final orders:", len(orders_df))