import os
os.environ["JAVA_HOME"] = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot"
os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["PATH"] += r";C:\hadoop\bin"

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("OlistGold").getOrCreate()

def silver(name):
    return spark.read.parquet(f"output/silver/{name}")

orders = silver("olist_orders_dataset")
items = silver("olist_order_items_dataset")
payments = silver("olist_order_payments_dataset")
products = silver("olist_products_dataset")
translation = silver("product_category_name_translation")

# One payment total per order
pay_total = payments.groupBy("order_id").agg(
    F.sum("payment_value").alias("order_payment_total")
)

# Product category in English
products = products.join(translation, "product_category_name", "left") \
    .select("product_id", "product_category_name_english")

# Join everything: one row per item sold
sales = (
    items
    .join(orders, "order_id", "left")
    .join(products, "product_id", "left")
    .join(pay_total, "order_id", "left")
    .select(
        "order_id", "order_item_id", "product_id",
        "product_category_name_english", "seller_id", "customer_id",
        "order_status", "order_purchase_timestamp",
        "price", "freight_value", "order_payment_total",
    )
)

sales.write.mode("overwrite").parquet("output/gold/sales")
print("Gold sales saved:", sales.count(), "rows")

spark.stop()