import pandas as pd
from pathlib import Path


# --------------------------------
# Configuration
# --------------------------------

PROCESSED_DIR = Path("data/processed")
CLEAN_DIR = PROCESSED_DIR / "clean"
REJECTED_DIR = PROCESSED_DIR / "rejected"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)
REJECTED_DIR.mkdir(parents=True, exist_ok=True)


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
# Convert data types
# --------------------------------

orders_df["order_date"] = pd.to_datetime(
    orders_df["order_date"],
    errors="coerce"
)


# --------------------------------
# Create validation flags
# --------------------------------

orders_df["rejection_reason"] = ""


# Missing customer ID
orders_df.loc[
    orders_df["customer_id"].isna(),
    "rejection_reason"
] = "missing_customer_id"


# Invalid quantity
orders_df.loc[
    orders_df["quantity"] <= 0,
    "rejection_reason"
] = "invalid_quantity"


# Invalid date
orders_df.loc[
    orders_df["order_date"].isna(),
    "rejection_reason"
] = "invalid_date"


# --------------------------------
# Referential integrity checks
# --------------------------------

valid_customer_ids = set(
    customers_df["customer_id"]
)

valid_product_ids = set(
    products_df["product_id"]
)


invalid_customer_reference = (
    ~orders_df["customer_id"].isin(
        valid_customer_ids
    )
    & orders_df["customer_id"].notna()
)


orders_df.loc[
    invalid_customer_reference,
    "rejection_reason"
] = "invalid_customer_reference"


invalid_product_reference = (
    ~orders_df["product_id"].isin(
        valid_product_ids
    )
)


orders_df.loc[
    invalid_product_reference,
    "rejection_reason"
] = "invalid_product_reference"


# --------------------------------
# Detect duplicate orders
# --------------------------------

duplicate_orders = orders_df.duplicated(
    subset=["order_id"],
    keep="first"
)

orders_df.loc[
    duplicate_orders,
    "rejection_reason"
] = "duplicate_order"


# --------------------------------
# Separate valid and rejected data
# --------------------------------

rejected_orders = orders_df[
    orders_df["rejection_reason"] != ""
].copy()


clean_orders = orders_df[
    orders_df["rejection_reason"] == ""
].copy()


# --------------------------------
# Remove validation column
# from clean dataset
# --------------------------------

clean_orders = clean_orders.drop(
    columns=["rejection_reason"]
)


# --------------------------------
# Join product price
# --------------------------------

clean_orders = clean_orders.merge(
    products_df[
        ["product_id", "price"]
    ],
    on="product_id",
    how="left"
)


# --------------------------------
# Calculate total amount
# --------------------------------

clean_orders["total_amount"] = (
    clean_orders["quantity"]
    * clean_orders["price"]
)


# --------------------------------
# Save clean data
# --------------------------------

customers_df.to_csv(
    CLEAN_DIR / "customers_clean.csv",
    index=False
)

products_df.to_csv(
    CLEAN_DIR / "products_clean.csv",
    index=False
)

clean_orders.to_csv(
    CLEAN_DIR / "orders_clean.csv",
    index=False
)


# --------------------------------
# Save rejected data
# --------------------------------

rejected_orders.to_csv(
    REJECTED_DIR / "orders_rejected.csv",
    index=False
)


# --------------------------------
# Print pipeline summary
# --------------------------------

print("\n======================================")
print("          CLEANING SUMMARY")
print("======================================")

print(
    "Input orders:",
    len(orders_df)
)

print(
    "Valid orders:",
    len(clean_orders)
)

print(
    "Rejected orders:",
    len(rejected_orders)
)

print("\nRejection reasons:")

print(
    rejected_orders[
        "rejection_reason"
    ].value_counts()
)

print("\nCleaning completed successfully.")