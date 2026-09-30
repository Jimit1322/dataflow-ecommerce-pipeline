import pandas as pd
import psycopg2
from pathlib import Path


# --------------------------------
# Configuration
# --------------------------------

DB_CONFIG = {
    "dbname": "dataflow",
    "user": "jimit",
    "host": "localhost",
    "port": 5432
}

CLEAN_DIR = Path("data/processed/clean")


# --------------------------------
# Load CSV files
# --------------------------------

customers_df = pd.read_csv(
    CLEAN_DIR / "customers_clean.csv"
)

products_df = pd.read_csv(
    CLEAN_DIR / "products_clean.csv"
)

orders_df = pd.read_csv(
    CLEAN_DIR / "orders_clean.csv"
)


print("Clean datasets loaded.")

print("Customers:", len(customers_df))
print("Products:", len(products_df))
print("Orders:", len(orders_df))


# --------------------------------
# Connect to PostgreSQL
# --------------------------------

connection = psycopg2.connect(
    **DB_CONFIG
)

cursor = connection.cursor()

print("Connected to PostgreSQL.")


# --------------------------------
# Load customers
# --------------------------------

for _, row in customers_df.iterrows():

    cursor.execute(
        """
        INSERT INTO customers
        (
            customer_id,
            name,
            city,
            email
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (customer_id)
        DO NOTHING;
        """,
        (
            row["customer_id"],
            row["name"],
            row["city"],
            row["email"]
        )
    )


# --------------------------------
# Load products
# --------------------------------

for _, row in products_df.iterrows():

    cursor.execute(
        """
        INSERT INTO products
        (
            product_id,
            product_name,
            category,
            price
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (product_id)
        DO NOTHING;
        """,
        (
            row["product_id"],
            row["product_name"],
            row["category"],
            row["price"]
        )
    )


# --------------------------------
# Load orders
# --------------------------------

for _, row in orders_df.iterrows():

    cursor.execute(
        """
        INSERT INTO orders
        (
            order_id,
            customer_id,
            product_id,
            quantity,
            order_date,
            price,
            total_amount
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (order_id)
        DO NOTHING;
        """,
        (
            row["order_id"],
            row["customer_id"],
            row["product_id"],
            row["quantity"],
            row["order_date"],
            row["price"],
            row["total_amount"]
        )
    )


# --------------------------------
# Commit changes
# --------------------------------

connection.commit()

print("Data loaded successfully.")


# --------------------------------
# Close connection
# --------------------------------

cursor.close()
connection.close()

print("PostgreSQL connection closed.")