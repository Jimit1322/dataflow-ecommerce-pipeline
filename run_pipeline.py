import subprocess
import sys
import time

from src.logger import get_logger


logger = get_logger("pipeline")


def run_step(description, command):

    logger.info("=" * 60)
    logger.info(description)
    logger.info("=" * 60)

    start_time = time.time()

    result = subprocess.run(
        [sys.executable] + command
    )

    if result.returncode != 0:
        logger.error("FAILED: %s", description)
        sys.exit(result.returncode)

    elapsed = time.time() - start_time

    logger.info(
        "COMPLETED: %s | Time: %.2f seconds",
        description,
        elapsed
    )


def main():

    logger.info("Starting DataFlow ETL pipeline")

    run_step(
        "1. Generating source data",
        ["src/generate_data.py"]
    )

    run_step(
        "2. Ingesting raw data",
        ["src/ingest.py"]
    )

    run_step(
        "3. Cleaning and transforming data",
        ["src/clean.py"]
    )

    run_step(
        "4. Validating data quality",
        ["src/validate.py"]
    )

    run_step(
        "5. Running PySpark transformations",
        ["pyspark/transform.py"]
    )

    run_step(
        "6. Loading data into PostgreSQL",
        ["src/load_to_postgres.py"]
    )
    
    run_step(
        "7. Generating analytics output",
        ["src/export_analytics.py"]
    )

    logger.info("DATA PIPELINE COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()