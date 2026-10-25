import os
os.environ["JAVA_HOME"] = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot"
os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["PATH"] += r";C:\hadoop\bin"

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("OlistSilver").getOrCreate()

tables = [
    "olist_orders_dataset",
    "olist_order_items_dataset",
    "olist_order_payments_dataset",
    "olist_order_reviews_dataset",
    "olist_products_dataset",
    "olist_sellers_dataset",
    "olist_geolocation_dataset",
    "product_category_name_translation",
]

for name in tables:
    df = spark.read.parquet(f"output/bronze/{name}")
    before = df.count()
    clean = df.dropDuplicates()
    clean.write.mode("overwrite").parquet(f"output/silver/{name}")
    print(name, "| before:", before, "| after:", clean.count())

spark.stop()