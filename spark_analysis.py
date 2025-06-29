import time
import sys
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Circuit Sensor Data Analysis") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

# Accept file path as argument
if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    input_file = 'realistic_circuit_sensor_data.csv'

print(f"Spark analysis starting with input file: {input_file}")

# Check if input file exists
if not os.path.exists(input_file):
    print(f"ERROR: Input file {input_file} does not exist!")
    sys.exit(1)

# Read the CSV file
print("Loading dataset...")
try:
    df = spark.read.csv(input_file, header=True, inferSchema=True)
    print(f"Dataset loaded successfully. Rows: {df.count()}, Columns: {len(df.columns)}")
except Exception as e:
    print(f"ERROR: Failed to load dataset: {e}")
    sys.exit(1)

# 1. Record start time for heat analysis
start_time = time.time()

# 1. Basic Data Analysis
print("\n=== Basic Data Analysis ===")
print("\nSchema:")
df.printSchema()

print("\nSummary Statistics:")
df.select("voltage(V)", "current(A)", "temperature(C)", "power(W)", "component_age(years)").summary().show()

# 2. Component Analysis
print("\n=== Component Analysis ===")
component_stats = df.groupBy("component") \
    .agg(
        count("*").alias("count"),
        avg("voltage(V)").alias("avg_voltage"),
        avg("current(A)").alias("avg_current"),
        avg("temperature(C)").alias("avg_temperature"),
        avg("power(W)").alias("avg_power")
    ) \
    .orderBy(desc("count"))

print("\nComponent Statistics:")
component_stats.show(truncate=False)

# 3. Fault Analysis
print("\n=== Fault Analysis ===")
fault_analysis = df.groupBy("component", "fault") \
    .count() \
    .orderBy("component", "fault")

print("\nFault Distribution by Component:")
fault_analysis.show(truncate=False)

# 4. Temperature Category Analysis
print("\n=== Temperature Category Analysis ===")
temp_analysis = df.groupBy("temperature_category") \
    .agg(
        count("*").alias("count"),
        avg("temperature(C)").alias("avg_temperature"),
        min("temperature(C)").alias("min_temperature"),
        max("temperature(C)").alias("max_temperature")
    ) \
    .orderBy("temperature_category")

print("\nTemperature Category Statistics:")
temp_analysis.show(truncate=False)

# 5. Time-based Analysis
print("\n=== Time-based Analysis ===")
# Convert timestamp to hour
df_with_hour = df.withColumn("hour", hour(to_timestamp("timestamp")))

hourly_analysis = df_with_hour.groupBy("hour") \
    .agg(
        avg("anomaly_score").alias("avg_anomaly_score"),
        avg("temperature(C)").alias("avg_temperature"),
        count("*").alias("record_count")
    ) \
    .orderBy("hour")

print("\nHourly Statistics:")
hourly_analysis.show(truncate=False)

# 6. Correlation Analysis
print("\n=== Correlation Analysis ===")
# Select numeric columns for correlation
numeric_cols = ["voltage(V)", "current(A)", "temperature(C)", "power(W)", "component_age(years)", "anomaly_score"]
correlation_matrix = df.select(numeric_cols).toPandas().corr()

print("\nCorrelation Matrix:")
print(correlation_matrix)

# 7. Anomaly Detection
print("\n=== Anomaly Detection ===")
# Define high anomaly threshold (e.g., 2 standard deviations)
anomaly_threshold = 2.0
high_anomalies = df.filter(abs(col("anomaly_score")) > anomaly_threshold) \
    .groupBy("component") \
    .count() \
    .orderBy(desc("count"))

print("\nHigh Anomaly Components:")
high_anomalies.show(truncate=False)

# 8. Power Consumption Analysis
print("\n=== Power Consumption Analysis ===")
power_analysis = df.groupBy("component") \
    .agg(
        avg("power(W)").alias("avg_power"),
        stddev("power(W)").alias("stddev_power"),
        min("power(W)").alias("min_power"),
        max("power(W)").alias("max_power")
    ) \
    .orderBy(desc("avg_power"))

print("\nPower Consumption Statistics:")
power_analysis.show(truncate=False)

# Save results to CSV files using Spark's coalesce(1).write.csv()
print("\nSaving results to CSV files...")

# Set output directory to circuit_dashboard/data/
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'circuit_dashboard', 'data')
os.makedirs(output_dir, exist_ok=True)
print(f"Output directory: {output_dir}")

try:
    # Fault statistics per component
    print("Saving fault statistics...")
    fault_stats = df.groupBy("component").agg(count(when(col("fault") == "Yes", True)).alias("fault_count"))
    fault_stats.coalesce(1).write.option("header", True).csv(os.path.join(output_dir, "spark_fault_stats.csv"), mode="overwrite")

    # Component-wise min/avg/max for voltage, temperature, power
    print("Saving component summary...")
    component_summary = df.groupBy("component").agg(
        min("voltage(V)").alias("min_voltage"),
        avg("voltage(V)").alias("avg_voltage"),
        max("voltage(V)").alias("max_voltage"),
        min("temperature(C)").alias("min_temperature"),
        avg("temperature(C)").alias("avg_temperature"),
        max("temperature(C)").alias("max_temperature"),
        min("power(W)").alias("min_power"),
        avg("power(W)").alias("avg_power"),
        max("power(W)").alias("max_power")
    )
    component_summary.coalesce(1).write.option("header", True).csv(os.path.join(output_dir, "component_summary.csv"), mode="overwrite")

    print("Saving temperature trends...")
    temp_trends = df.groupBy("temperature_category").agg(count("*").alias("count"))
    temp_trends.coalesce(1).write.option("header", True).csv(os.path.join(output_dir, "temperature_trends.csv"), mode="overwrite")

    # Faults over time (by timestamp or index)
    print("Saving time trend...")
    time_trend = df.select("timestamp", "fault")
    time_trend.coalesce(1).write.option("header", True).csv(os.path.join(output_dir, "time_trend.csv"), mode="overwrite")

    # Correlation matrix for visualization
    print("Saving correlation matrix...")
    correlation_matrix_pd = df.select(numeric_cols).toPandas().corr()
    correlation_matrix_pd.to_csv(os.path.join(output_dir, "correlation_matrix.csv"))

    # Also save the original outputs for compatibility
    print("Saving component stats...")
    component_stats.coalesce(1).write.option("header", True).csv(os.path.join(output_dir, "spark_component_stats.csv"), mode="overwrite")
    
    print("Saving fault analysis...")
    fault_analysis.coalesce(1).write.option("header", True).csv(os.path.join(output_dir, "spark_fault_analysis.csv"), mode="overwrite")
    
    print("Saving temp analysis...")
    temp_analysis.coalesce(1).write.option("header", True).csv(os.path.join(output_dir, "spark_temp_analysis.csv"), mode="overwrite")
    
    print("Saving hourly analysis...")
    hourly_analysis.coalesce(1).write.option("header", True).csv(os.path.join(output_dir, "spark_hourly_analysis.csv"), mode="overwrite")
    
    print("Saving power analysis...")
    power_analysis.coalesce(1).write.option("header", True).csv(os.path.join(output_dir, "spark_power_analysis.csv"), mode="overwrite")

    # 2. Heat Generation Analysis
    end_time = time.time()
    processing_time = end_time - start_time
    estimated_heat = processing_time * 0.75

    print("Saving heat analysis...")
    import csv
    with open(os.path.join(output_dir, 'heat_analysis.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['processing_time', 'estimated_heat'])
        writer.writerow([processing_time, estimated_heat])

    print("\nAnalysis complete! Results saved to CSV files.")
    print(f"All files saved to: {output_dir}")

except Exception as e:
    print(f"ERROR: Failed to save results: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Stop Spark session
spark.stop() 