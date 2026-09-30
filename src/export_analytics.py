import pandas as pd
import psycopg2
import os


DB_CONFIG = {
    "dbname": "dataflow",
    "user": "jimit",
    "host": "localhost",
    "port": "5432"
}


def main():

    os.makedirs("data/output", exist_ok=True)

    conn = psycopg2.connect(**DB_CONFIG)

    query = """
        SELECT
            p.category,
            COUNT(o.order_id) AS total_orders,
            SUM(o.quantity) AS units_sold,
            ROUND(SUM(o.total_amount), 2) AS revenue
        FROM orders o
        JOIN products p
            ON o.product_id = p.product_id
        GROUP BY p.category
        ORDER BY revenue DESC;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    output_path = "data/output/category_revenue.csv"

    df.to_csv(output_path, index=False)

    print("\nCategory Revenue:")
    print(df)

    print(f"\nAnalytics exported to: {output_path}")


if __name__ == "__main__":
    main()