import os
import pandas as pd
import numpy as np

def map_power(row):
    """Map function to emit (component, (power, 1))"""
    return (row['component'], (row['power(W)'], 1))

def reduce_power(component, power_counts):
    """Reduce function to calculate average power"""
    total_power = sum(power for power, _ in power_counts)
    total_count = sum(count for _, count in power_counts)
    return total_power / total_count if total_count > 0 else 0

# Use current directory since script runs with cwd=parent_dir
data_path = 'realistic_circuit_sensor_data.csv'
print(f"Loading dataset from: {data_path}")
df = pd.read_csv(data_path)

# Map phase
print("Loading dataset...")
print("\nPerforming Map phase...")
mapped_data = df.apply(map_power, axis=1)

# Reduce phase
print("Performing Reduce phase...")
power_data = {}
for component, (power, count) in mapped_data:
    if component not in power_data:
        power_data[component] = []
    power_data[component].append((power, count))

# Calculate final results
results = {component: reduce_power(component, power_counts) 
           for component, power_counts in power_data.items()}

# Print results
print("\n=== Average Power Consumption Results ===")
print("\nAverage Power per Component (Watts):")
for component, avg_power in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(f"{component}: {avg_power:.4f}W")

# Save results to CSV
results_df = pd.DataFrame({
    'Component': results.keys(),
    'Average_Power_Watts': results.values()
})
# Save to circuit_dashboard/data directory
circuit_dashboard_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'circuit_dashboard', 'data')
# Ensure the directory exists
os.makedirs(circuit_dashboard_data_dir, exist_ok=True)
results_df.to_csv(os.path.join(circuit_dashboard_data_dir, 'power_analysis_results.csv'), index=False)
print(f"\nResults saved to '{os.path.join(circuit_dashboard_data_dir, 'power_analysis_results.csv')}'") 