from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path


# ----------------------------------------
# Create Spark session
# ----------------------------------------

spark = (
    SparkSession.builder
    .appName("DataFlow-Ecommerce-Pipeline")
    .master("local[*]")
    .getOrCreate()
)


print("Spark session created successfully.")

CLEAN_DIR = Path("data/processed/clean")

orders_df = spark.read.csv(
    str(CLEAN_DIR / "orders_clean.csv"),
    header=True,
    inferSchema=True
)

products_df = spark.read.csv(
    str(CLEAN_DIR / "products_clean.csv"),
    header=True,
    inferSchema=True
)

customers_df = spark.read.csv(
    str(CLEAN_DIR / "customers_clean.csv"),
    header=True,
    inferSchema=True
)

print("\n========== ORDERS SCHEMA ==========")
orders_df.printSchema()

print("\n========== PRODUCTS SCHEMA ==========")
products_df.printSchema()

print("\n========== CUSTOMERS SCHEMA ==========")
customers_df.printSchema()


print("\n========== RECORD COUNTS ==========")

print("Customers:", customers_df.count())
print("Products:", products_df.count())
print("Orders:", orders_df.count())

orders_df = orders_df.withColumn(
    "order_date",
    F.to_date("order_date")
)
orders_df = (
    orders_df
    .withColumn("order_year", F.year("order_date"))
    .withColumn("order_month", F.month("order_date"))
    .withColumn("order_day", F.dayofmonth("order_date"))
    .withColumn("order_day_of_week", F.dayofweek("order_date"))
)

orders_enriched = orders_df.join(
    products_df.select(
        "product_id",
        "product_name",
        "category"
    ),
    on="product_id",
    how="left"
)

orders_enriched = orders_enriched.join(
    customers_df.select(
        "customer_id",
        "city"
    ),
    on="customer_id",
    how="left"
)
orders_enriched = orders_enriched.withColumn(
    "total_amount",
    F.col("quantity") * F.col("price")
)
orders_enriched = orders_enriched.dropDuplicates(
    ["order_id"]
)
orders_enriched = orders_enriched.filter(
    (F.col("quantity") > 0) &
    (F.col("price") > 0) &
    (F.col("total_amount") > 0)
)
print("\n========== TRANSFORMED DATA ==========")

orders_enriched.show(
    10,
    truncate=False
)
print("\nFinal record count:")
print(orders_enriched.count())

daily_sales = (
    orders_enriched
    .groupBy(
        "order_date"
    )
    .agg(
        F.sum("total_amount").alias("daily_revenue"),
        F.countDistinct("order_id").alias("total_orders"),
        F.sum("quantity").alias("items_sold")
    )
    .orderBy("order_date")
)
print("\n========== DAILY SALES ==========")

daily_sales.show(20)

category_sales = (
    orders_enriched
    .groupBy("category")
    .agg(
        F.sum("total_amount").alias("revenue"),
        F.sum("quantity").alias("units_sold"),
        F.countDistinct("order_id").alias("orders")
    )
    .orderBy(
        F.desc("revenue")
    )
)
print("\n========== CATEGORY SALES ==========")

category_sales.show()

OUTPUT_DIR = Path("data/output")
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

orders_enriched.write \
    .mode("overwrite") \
    .parquet(
        str(OUTPUT_DIR / "orders")
    )
    
daily_sales.write \
    .mode("overwrite") \
    .parquet(
        str(OUTPUT_DIR / "daily_sales")
    )
    
category_sales.write \
    .mode("overwrite") \
    .parquet(
        str(OUTPUT_DIR / "category_sales")
    )
    
print("\n========== READING PARQUET ==========")

saved_orders = spark.read.parquet(
    str(OUTPUT_DIR / "orders")
)

saved_orders.printSchema()

print(
    "Saved records:",
    saved_orders.count()
)
saved_orders.show(5)

spark.stop()