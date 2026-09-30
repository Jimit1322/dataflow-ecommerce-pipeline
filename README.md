# DataFlow - E-commerce Data Engineering Pipeline

An end-to-end data engineering pipeline built using Python, Pandas, PySpark and PostgreSQL.

The project demonstrates data ingestion, cleaning, validation, distributed data transformation, analytical database loading and SQL-based analytics.

---

## Tech Stack

- Python
- Pandas
- PySpark
- PostgreSQL
- SQL
- Parquet
- Git

---

## Project Architecture

```text
CSV / JSON Source Data
          |
          v
      Ingestion
          |
          v
 Cleaning & Validation
          |
          v
       PySpark
    Transformations
          |
     +----+----+
     |         |
     v         v
  Parquet   PostgreSQL
               |
               v
           SQL Analytics
               |
               v
        Analytics Output