import pandas as pd
from pathlib import Path


RAW_DIR = Path("data/raw")

orders_path = RAW_DIR / "orders.csv"

orders_df = pd.read_csv(orders_path)

print("Original records:", len(orders_df))


# ------------------------------------------------
# 1. Duplicate an existing order
# ------------------------------------------------

duplicate_row = orders_df.iloc[[0]].copy()

orders_df = pd.concat(
    [orders_df, duplicate_row],
    ignore_index=True
)


# ------------------------------------------------
# 2. Missing customer ID
# ------------------------------------------------

orders_df.loc[
    orders_df.index[-1],
    "customer_id"
] = None


# ------------------------------------------------
# 3. Invalid quantity
# ------------------------------------------------

orders_df.loc[
    orders_df.index[-2],
    "quantity"
] = -5


# ------------------------------------------------
# 4. Invalid date
# ------------------------------------------------

orders_df.loc[
    orders_df.index[-3],
    "order_date"
] = "INVALID_DATE"


# ------------------------------------------------
# 5. Non-existing customer
# ------------------------------------------------

orders_df.loc[
    orders_df.index[-4],
    "customer_id"
] = "C999999"


# ------------------------------------------------
# Save
# ------------------------------------------------

orders_df.to_csv(
    orders_path,
    index=False
)

print("Bad data injected successfully.")
print("New records:", len(orders_df))