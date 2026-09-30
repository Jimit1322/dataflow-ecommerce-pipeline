import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path


RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Sample data
# -----------------------------

cities = [
    "Jaipur",
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Ahmedabad",
    "Pune",
    "Hyderabad",
    "Chennai",
]

first_names = [
    "Rahul",
    "Priya",
    "Amit",
    "Neha",
    "Rohan",
    "Ananya",
    "Arjun",
    "Karan",
]

last_names = [
    "Sharma",
    "Mehta",
    "Patel",
    "Verma",
    "Joshi",
    "Gupta",
]

products = [
    ("P001", "Wireless Mouse", "Electronics", 599),
    ("P002", "Keyboard", "Electronics", 999),
    ("P003", "Notebook", "Stationery", 199),
    ("P004", "Water Bottle", "Home", 399),
    ("P005", "USB Cable", "Electronics", 299),
    ("P006", "Backpack", "Fashion", 1299),
    ("P007", "Desk Lamp", "Home", 899),
    ("P008", "Pen Set", "Stationery", 149),
    ("P009", "Headphones", "Electronics", 1499),
    ("P010", "Phone Stand", "Electronics", 499),
]


# -----------------------------
# Generate customers
# -----------------------------

customers = []

for i in range(1, 1001):

    first = random.choice(first_names)
    last = random.choice(last_names)

    customers.append({
        "customer_id": f"C{i:04d}",
        "name": f"{first} {last}",
        "city": random.choice(cities),
        "email": f"{first.lower()}.{last.lower()}{i}@example.com"
    })


with open(RAW_DIR / "customers.json", "w") as file:
    json.dump(customers, file, indent=2)


# -----------------------------
# Generate products
# -----------------------------

with open(RAW_DIR / "products.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "product_id",
        "product_name",
        "category",
        "price"
    ])

    for product in products:
        writer.writerow(product)


# -----------------------------
# Generate orders
# -----------------------------

start_date = datetime(2026, 1, 1)

with open(RAW_DIR / "orders.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "order_id",
        "customer_id",
        "product_id",
        "quantity",
        "order_date"
    ])

    for i in range(1, 100001):

        customer_id = random.choice(customers)["customer_id"]
        product = random.choice(products)

        product_id = product[0]

        quantity = random.randint(1, 5)

        order_date = start_date + timedelta(
            days=random.randint(0, 180)
        )

        writer.writerow([
            f"O{i:06d}",
            customer_id,
            product_id,
            quantity,
            order_date.strftime("%Y-%m-%d")
        ])


print("Dataset generated successfully.")
print("Customers:", len(customers))
print("Products:", len(products))
print("Orders: 100000")