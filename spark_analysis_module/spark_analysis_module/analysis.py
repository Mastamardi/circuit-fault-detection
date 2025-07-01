import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, hour, to_timestamp

# Paths
DATA_PATH = 'spark_analysis_module/data/realistic_circuit_sensor_data.csv'
RESULTS_DIR = 'results'

# Ensure results directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)

# Initialize Spark session
spark = SparkSession.builder.appName('CircuitBoardAnalysis').getOrCreate()

def load_data():
    return spark.read.option('header', True).option('inferSchema', True).csv(DATA_PATH)

def analyze_fault_frequency(df):
    # Fault Frequency by Component
    faults = (
        df.filter(col('fault') == 'Yes')
          .groupBy('component')
          .agg(count('*').alias('fault_count'))
          .orderBy(col('fault_count').desc())
    )
    faults.toPandas().to_csv(f'{RESULTS_DIR}/faults.csv', index=False)
    return faults

def analyze_power_consumption(df):
    # Average Power Consumption by Component
    power = (
        df.groupBy('component')
          .agg(avg(col('power(W)')).alias('avg_power_W'))
          .orderBy(col('avg_power_W').desc())
    )
    power.toPandas().to_csv(f'{RESULTS_DIR}/power.csv', index=False)
    return power

def analyze_temperature_by_category(df):
    # Average Temperature by Temperature Category
    temp = (
        df.groupBy('temperature_category')
          .agg(avg(col('temperature(C)')).alias('avg_temp_C'))
          .orderBy(col('avg_temp_C').desc())
    )
    temp.toPandas().to_csv(f'{RESULTS_DIR}/temp.csv', index=False)
    return temp

def analyze_hourly_anomaly(df):
    # Hourly Trend of Anomaly Score
    df_with_hour = df.withColumn('hour', hour(to_timestamp(col('timestamp'))))
    anomaly = (
        df_with_hour.groupBy('hour')
            .agg(avg(col('anomaly_score')).alias('avg_anomaly_score'))
            .orderBy('hour')
    )
    anomaly.toPandas().to_csv(f'{RESULTS_DIR}/anomaly.csv', index=False)
    return anomaly

def main():
    df = load_data()
    print('Data loaded.')
    faults = analyze_fault_frequency(df)
    print('Fault frequency by component saved.')
    power = analyze_power_consumption(df)
    print('Average power consumption by component saved.')
    temp = analyze_temperature_by_category(df)
    print('Average temperature by category saved.')
    anomaly = analyze_hourly_anomaly(df)
    print('Hourly anomaly score trend saved.')
    print('All analyses complete.')

if __name__ == '__main__':
    main() 