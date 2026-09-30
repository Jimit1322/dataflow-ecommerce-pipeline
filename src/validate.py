import pandas as pd
from pathlib import Path


PROCESSED_DIR = Path("data/processed")

RAW_ORDERS = pd.read_csv(
    PROCESSED_DIR / "orders_ingested.csv"
)

CLEAN_ORDERS = pd.read_csv(
    PROCESSED_DIR / "clean" / "orders_clean.csv"
)

REJECTED_ORDERS = pd.read_csv(
    PROCESSED_DIR / "rejected" / "orders_rejected.csv"
)

CUSTOMERS = pd.read_csv(
    PROCESSED_DIR / "clean" / "customers_clean.csv"
)

PRODUCTS = pd.read_csv(
    PROCESSED_DIR / "clean" / "products_clean.csv"
)


print("======================================")
print("       DATA QUALITY REPORT")
print("======================================")


# --------------------------------
# Raw data
# --------------------------------

print("\nRAW ORDERS")

print(
    "Total records:",
    len(RAW_ORDERS)
)

print(
    "Duplicate order IDs:",
    RAW_ORDERS["order_id"].duplicated().sum()
)

print(
    "Missing customer IDs:",
    RAW_ORDERS["customer_id"].isna().sum()
)

print(
    "Invalid quantities:",
    (RAW_ORDERS["quantity"] <= 0).sum()
)


# --------------------------------
# Rejected records
# --------------------------------

print("\nREJECTED RECORDS")

print(
    "Total rejected:",
    len(REJECTED_ORDERS)
)

print(
    REJECTED_ORDERS[
        "rejection_reason"
    ].value_counts()
)


# --------------------------------
# Clean data
# --------------------------------

print("\nCLEAN DATA")

print(
    "Valid records:",
    len(CLEAN_ORDERS)
)

print(
    "Duplicate order IDs:",
    CLEAN_ORDERS["order_id"].duplicated().sum()
)

print(
    "Missing customer IDs:",
    CLEAN_ORDERS["customer_id"].isna().sum()
)

print(
    "Invalid quantities:",
    (
        CLEAN_ORDERS["quantity"] <= 0
    ).sum()
)


# --------------------------------
# Referential integrity
# --------------------------------

valid_customer_ids = set(
    CUSTOMERS["customer_id"]
)

valid_product_ids = set(
    PRODUCTS["product_id"]
)


invalid_customers = (
    ~CLEAN_ORDERS["customer_id"].isin(
        valid_customer_ids
    )
).sum()


invalid_products = (
    ~CLEAN_ORDERS["product_id"].isin(
        valid_product_ids
    )
).sum()


print(
    "Invalid customer references:",
    invalid_customers
)

print(
    "Invalid product references:",
    invalid_products
)


# --------------------------------
# Final status
# --------------------------------

print("\n======================================")

if (
    len(REJECTED_ORDERS) > 0
    and
    len(CLEAN_ORDERS) > 0
):

    print(
        "DATA QUALITY PIPELINE PASSED"
    )

else:

    print(
        "DATA QUALITY PIPELINE FAILED"
    )

print("======================================")