import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set the style
plt.style.use('seaborn-v0_8')
sns.set_theme(style="whitegrid")

# Read the CSV files
component_stats = pd.read_csv('spark_component_stats.csv')
fault_analysis = pd.read_csv('spark_fault_analysis.csv')
temp_analysis = pd.read_csv('spark_temp_analysis.csv')
hourly_analysis = pd.read_csv('spark_hourly_analysis.csv')
power_analysis = pd.read_csv('spark_power_analysis.csv')

# Create a figure with subplots
plt.figure(figsize=(20, 15))

# 1. Component Distribution and Power Consumption
plt.subplot(2, 2, 1)
sns.barplot(data=component_stats, x='component', y='avg_power')
plt.xticks(rotation=45, ha='right')
plt.title('Average Power Consumption by Component')
plt.xlabel('Component')
plt.ylabel('Average Power (W)')
plt.tight_layout()

# 2. Temperature Categories
plt.subplot(2, 2, 2)
sns.barplot(data=temp_analysis, x='temperature_category', y='count')
plt.title('Number of Records by Temperature Category')
plt.xlabel('Temperature Category')
plt.ylabel('Count')
plt.tight_layout()

# 3. Fault Distribution
plt.subplot(2, 2, 3)
fault_pivot = fault_analysis.pivot(index='component', columns='fault', values='count')
fault_pivot.plot(kind='bar', stacked=True)
plt.title('Fault Distribution by Component')
plt.xlabel('Component')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Fault Status')
plt.tight_layout()

# 4. Hourly Anomaly Scores
plt.subplot(2, 2, 4)
sns.lineplot(data=hourly_analysis, x='hour', y='avg_anomaly_score', marker='o')
plt.title('Average Anomaly Score by Hour')
plt.xlabel('Hour of Day')
plt.ylabel('Average Anomaly Score')
plt.xticks(range(0, 24))
plt.grid(True)
plt.tight_layout()

# Save the first figure
plt.savefig('analysis_overview.png', dpi=300, bbox_inches='tight')
plt.close()

# Create a second figure for detailed analysis
plt.figure(figsize=(20, 15))

# 5. Power Consumption Statistics
plt.subplot(2, 2, 1)
power_melted = power_analysis.melt(id_vars=['component'], 
                                 value_vars=['min_power', 'avg_power', 'max_power'],
                                 var_name='Power Type', 
                                 value_name='Power (W)')
sns.boxplot(data=power_melted, x='component', y='Power (W)', hue='Power Type')
plt.title('Power Consumption Statistics by Component')
plt.xlabel('Component')
plt.ylabel('Power (W)')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Power Type')
plt.tight_layout()

# 6. Temperature Distribution
plt.subplot(2, 2, 2)
sns.boxplot(data=temp_analysis, x='temperature_category', y='avg_temperature')
plt.title('Temperature Distribution by Category')
plt.xlabel('Temperature Category')
plt.ylabel('Temperature (°C)')
plt.tight_layout()

# 7. Component Age vs Power
plt.subplot(2, 2, 3)
sns.scatterplot(data=component_stats, x='component_age(years)', y='avg_power', 
                hue='component', size='count', sizes=(50, 400))
plt.title('Component Age vs Power Consumption')
plt.xlabel('Component Age (years)')
plt.ylabel('Average Power (W)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# 8. Hourly Temperature Trends
plt.subplot(2, 2, 4)
sns.lineplot(data=hourly_analysis, x='hour', y='avg_temperature', marker='o')
plt.title('Average Temperature by Hour')
plt.xlabel('Hour of Day')
plt.ylabel('Temperature (°C)')
plt.xticks(range(0, 24))
plt.grid(True)
plt.tight_layout()

# Save the second figure
plt.savefig('detailed_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Create a third figure for correlation analysis
plt.figure(figsize=(15, 10))

# 9. Correlation Heatmap
numeric_cols = ['voltage(V)', 'current(A)', 'temperature(C)', 'power(W)', 
                'component_age(years)', 'anomaly_score']
correlation_matrix = component_stats[numeric_cols].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix of Numeric Variables')
plt.tight_layout()

# Save the third figure
plt.savefig('correlation_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("Visualizations have been saved as:")
print("1. analysis_overview.png")
print("2. detailed_analysis.png")
print("3. correlation_analysis.png") 