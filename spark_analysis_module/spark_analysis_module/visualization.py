import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

RESULTS_DIR = 'results'
VISUALS_DIR = 'visuals'

os.makedirs(VISUALS_DIR, exist_ok=True)

interpretations = []

def plot_faults():
    df = pd.read_csv(f'{RESULTS_DIR}/faults.csv')
    if df.empty:
        interpretations.append("No fault data available to plot or interpret.")
        print('No data in faults.csv to plot.')
        return
    plt.figure(figsize=(8,6))
    sns.barplot(x='component', y='fault_count', data=df, palette='viridis')
    plt.title('Fault Frequency by Component')
    plt.ylabel('Fault Count')
    plt.xlabel('Component')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{VISUALS_DIR}/faults.png')
    # Interpretation
    top = df.iloc[0]
    interpretations.append(f"{top['component']} had the highest fault frequency, indicating potential reliability issues. Components with lower fault counts are more stable.")

def plot_power():
    df = pd.read_csv(f'{RESULTS_DIR}/power.csv')
    if df.empty:
        interpretations.append("No power consumption data available to plot or interpret.")
        print('No data in power.csv to plot.')
        return
    plt.figure(figsize=(8,6))
    plt.pie(df['avg_power_W'], labels=df['component'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title('Average Power Consumption by Component')
    plt.tight_layout()
    plt.savefig(f'{VISUALS_DIR}/power.png')
    # Interpretation
    max_idx = df['avg_power_W'].idxmax()
    interpretations.append(f"{df.loc[max_idx, 'component']} consumes the most power on average. Power distribution is uneven among components, which may affect energy efficiency.")

def plot_temp():
    df = pd.read_csv(f'{RESULTS_DIR}/temp.csv')
    if df.empty:
        interpretations.append("No temperature data available to plot or interpret.")
        print('No data in temp.csv to plot.')
        return
    plt.figure(figsize=(7,5))
    sns.barplot(x='temperature_category', y='avg_temp_C', data=df, palette='coolwarm')
    plt.title('Average Temperature by Category')
    plt.ylabel('Average Temperature (°C)')
    plt.xlabel('Temperature Category')
    plt.tight_layout()
    plt.savefig(f'{VISUALS_DIR}/temp.png')
    # Interpretation
    hottest = df.iloc[df['avg_temp_C'].idxmax()]
    interpretations.append(f"The '{hottest['temperature_category']}' category has the highest average temperature, suggesting these conditions are most thermally stressed.")

def plot_anomaly():
    df = pd.read_csv(f'{RESULTS_DIR}/anomaly.csv')
    if df.empty:
        interpretations.append("No anomaly score data available to plot or interpret.")
        print('No data in anomaly.csv to plot.')
        return
    plt.figure(figsize=(8,5))
    sns.lineplot(x='hour', y='avg_anomaly_score', data=df, marker='o')
    plt.title('Hourly Trend of Anomaly Score')
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Anomaly Score')
    plt.xticks(range(0,24))
    plt.tight_layout()
    plt.savefig(f'{VISUALS_DIR}/anomaly.png')
    # Interpretation
    peak_hour = df.iloc[df['avg_anomaly_score'].idxmax()]['hour']
    interpretations.append(f"Anomaly scores peak around hour {int(peak_hour)}, indicating increased irregularities during this period. Monitoring is advised at these times.")

def save_interpretations():
    with open(f'{RESULTS_DIR}/interpretations.txt', 'w') as f:
        for interp in interpretations:
            f.write(interp + '\n')
    print("Interpretations saved to results/interpretations.txt")

def main():
    plot_faults()
    print('Faults bar chart saved.')
    plot_power()
    print('Power pie chart saved.')
    plot_temp()
    print('Temperature bar chart saved.')
    plot_anomaly()
    print('Anomaly line chart saved.')
    save_interpretations()
    print('All visualizations and interpretations complete.')

if __name__ == '__main__':
    main() 