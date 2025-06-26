import pandas as pd
import numpy as np

def map_temperature(row):
    """Map function to emit (temperature_category, (temperature, 1))"""
    return (row['temperature_category'], (row['temperature(C)'], 1))

def reduce_temperature(category, temp_counts):
    """Reduce function to calculate average temperature"""
    total_temp = sum(temp for temp, _ in temp_counts)
    total_count = sum(count for _, count in temp_counts)
    return total_temp / total_count if total_count > 0 else 0

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('realistic_circuit_sensor_data.csv')

# Map phase
print("\nPerforming Map phase...")
mapped_data = df.apply(map_temperature, axis=1)

# Reduce phase
print("Performing Reduce phase...")
temp_data = {}
for category, (temp, count) in mapped_data:
    if category not in temp_data:
        temp_data[category] = []
    temp_data[category].append((temp, count))

# Calculate final results
results = {category: reduce_temperature(category, temp_counts) 
           for category, temp_counts in temp_data.items()}

# Print results
print("\n=== Temperature Category Analysis Results ===")
print("\nAverage Temperature per Category (°C):")
for category, avg_temp in sorted(results.items()):
    print(f"{category}: {avg_temp:.2f}°C")

# Save results to CSV
results_df = pd.DataFrame({
    'Temperature_Category': results.keys(),
    'Average_Temperature_C': results.values()
})
results_df.to_csv('temperature_analysis_results.csv', index=False)
print("\nResults saved to 'temperature_analysis_results.csv'") 