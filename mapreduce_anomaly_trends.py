import pandas as pd
import numpy as np
from datetime import datetime

def map_anomaly(row):
    """Map function to emit (hour, anomaly_score)"""
    timestamp = pd.to_datetime(row['timestamp'])
    hour = timestamp.hour
    return (hour, row['anomaly_score'])

def reduce_anomaly(hour, scores):
    """Reduce function to calculate average anomaly score per hour"""
    return np.mean(scores)

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('realistic_circuit_sensor_data.csv')

# Map phase
print("\nPerforming Map phase...")
mapped_data = df.apply(map_anomaly, axis=1)

# Reduce phase
print("Performing Reduce phase...")
anomaly_data = {}
for hour, score in mapped_data:
    if hour not in anomaly_data:
        anomaly_data[hour] = []
    anomaly_data[hour].append(score)

# Calculate final results
results = {hour: reduce_anomaly(hour, scores) 
           for hour, scores in anomaly_data.items()}

# Print results
print("\n=== Anomaly Score Trends by Hour ===")
print("\nAverage Anomaly Score per Hour:")
for hour in sorted(results.keys()):
    print(f"Hour {hour:02d}:00 - {hour:02d}:59: {results[hour]:.4f}")

# Save results to CSV
results_df = pd.DataFrame({
    'Hour': results.keys(),
    'Average_Anomaly_Score': results.values()
})
results_df.to_csv('anomaly_trends_results.csv', index=False)
print("\nResults saved to 'anomaly_trends_results.csv'") 