Olist E-Commerce Data Pipeline on AWS

An end-to-end data engineering project: raw CSV files go through a Bronze → Silver → Gold PySpark pipeline, land in Amazon S3, are queried with Amazon Athena, and are reported in a Power BI dashboard.

Dataset: Olist Brazilian E-Commerce (public, on Kaggle). About 100K orders and 112K items sold.

Dashboard

Architecture
CSV files (8 tables)
      |
      v
PySpark  ->  Bronze (raw Parquet)
         ->  Silver (cleaned, duplicates removed)
         ->  Gold   (one joined sales table)
      |
      v
Amazon S3  (bronze/  silver/  gold/)
      |
      v
Amazon Athena  (database: olist, table: gold_sales)
      |
      v
Power BI  (ODBC connection, star schema, DAX measures)
Tech stack
PySpark for the transformations
Amazon S3 as the data lake
Amazon Athena for SQL on the Gold layer
Power BI (DAX, star schema) for reporting
GitHub Actions for CI (runs on every push)
The pipeline
Layer	Script	What it does
Bronze	src/process_data.py	Reads the 8 CSV files and saves them as Parquet, unchanged
Silver	src/silver.py	Removes duplicate rows (for example, about 262K duplicates in the geolocation table)
Gold	src/gold.py	Joins orders, items, payments, products and category names into one table with one row per item sold (112,650 rows)
Data model (Power BI)

A star schema with one fact table and five dimensions:

gold_sales (fact)
Dim_Date, Dim_Product, Dim_Seller, Dim_Customer, Dim_Order_Status

The report uses 30+ DAX measures, such as Total Revenue, Total Orders, Average Order Value, Total Freight, Delivered Orders %, and insight text that changes with the filters.

How to run it
Download the Olist CSV files from Kaggle and put them in a folder called data/.
Install Python, Java 21 and PySpark (pip install pyspark).
Run the three steps in order:
python src/process_data.py
python src/silver.py
python src/gold.py

The Parquet files are written to output/bronze, output/silver and output/gold.

Upload them to your S3 bucket with the AWS CLI:
aws s3 sync output/bronze s3://YOUR_BUCKET/bronze/
aws s3 sync output/silver s3://YOUR_BUCKET/silver/
aws s3 sync output/gold   s3://YOUR_BUCKET/gold/
In Athena, create a database and an external table over gold/sales/, then connect Power BI through the Athena ODBC driver.

On Windows, PySpark also needs winutils.exe and hadoop.dll in a HADOOP_HOME\bin folder to write files.

Notes
The CSV files and the output/ folder are not in this repo (see .gitignore).
No AWS keys or passwords are stored in this repo.
