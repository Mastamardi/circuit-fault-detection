import os
import pandas as pd
import numpy as np

def map_faults(row):
    """Map function to emit (component, 1) for faulty components"""
    if row['fault'] == 'Yes':
        return (row['component'], 1)
    return (row['component'], 0)

def reduce_faults(component, counts):
    """Reduce function to sum fault counts per component"""
    return sum(counts)

# Use current directory since script runs with cwd=parent_dir
data_path = 'realistic_circuit_sensor_data.csv'
print(f"Loading dataset from: {data_path}")
df = pd.read_csv(data_path)

# Map phase
print("\nPerforming Map phase...")
mapped_data = df.apply(map_faults, axis=1)

# Reduce phase
print("Performing Reduce phase...")
fault_counts = {}
for component, count in mapped_data:
    if component not in fault_counts:
        fault_counts[component] = []
    fault_counts[component].append(count)

# Calculate final results
results = {component: reduce_faults(component, counts) 
           for component, counts in fault_counts.items()}

# Calculate percentages
total_records = len(df)
fault_percentages = {component: (count/total_records)*100 
                    for component, count in results.items()}

# Print results
print("\n=== Fault Analysis Results ===")
print("\nFault Counts per Component:")
for component, count in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(f"{component}: {count} faults ({fault_percentages[component]:.2f}%)")

# Save results to CSV
results_df = pd.DataFrame({
    'Component': results.keys(),
    'Fault_Count': results.values(),
    'Fault_Percentage': fault_percentages.values()
})
# Save to circuit_dashboard/data directory
circuit_dashboard_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'circuit_dashboard', 'data')
# Ensure the directory exists
os.makedirs(circuit_dashboard_data_dir, exist_ok=True)
results_df.to_csv(os.path.join(circuit_dashboard_data_dir, 'fault_analysis_results.csv'), index=False)
print(f"\nResults saved to '{os.path.join(circuit_dashboard_data_dir, 'fault_analysis_results.csv')}'") 