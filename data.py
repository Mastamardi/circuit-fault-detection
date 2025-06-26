import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Define component types
resistor_types = [
    "Carbon Composition Resistor", "Metal Film Resistor", "Wire Wound Resistor",
    "Thick Film Resistor", "Thin Film Resistor",
    "Potentiometer", "Rheostat", "Trimmer"
]

capacitor_types = ["Electrolytic Capacitor", "Ceramic Capacitor", "Tantalum Capacitor"]
ic_types = ["IC555 Timer", "OpAmp IC", "Microcontroller IC", "Voltage Regulator IC"]
power_module_types = ["Buck Converter", "Boost Converter", "Inverter Module"]

component_list = resistor_types + capacitor_types + ic_types + power_module_types

# Temperature category thresholds
def get_temp_category(temp):
    if temp < 40:
        return "Low"
    elif 40 <= temp <= 70:
        return "Normal"
    else:
        return "High"

# Generate data
n_records = 80000  # Updated to 80,000
start_time = datetime(2025, 4, 16, 6, 51, 34)

data = []

for i in range(n_records):
    component = random.choice(component_list)

    # Set parameter ranges based on component type
    if "Resistor" in component:
        voltage = round(random.uniform(3, 10), 2)
        current = round(random.uniform(0.01, 1.5), 2)
        temperature = round(random.uniform(30, 85), 2)
    elif "Capacitor" in component:
        voltage = round(random.uniform(4, 16), 2)
        current = round(random.uniform(0.1, 2.5), 2)
        temperature = round(random.uniform(25, 80), 2)
    elif "IC" in component:
        voltage = round(random.uniform(5, 12), 2)
        current = round(random.uniform(0.2, 1.0), 2)
        temperature = round(random.uniform(30, 95), 2)
    else:  # Power Module
        voltage = round(random.uniform(2, 15), 2)
        current = round(random.uniform(0.1, 3.0), 2)
        temperature = round(random.uniform(35, 90), 2)

    power = round(voltage * current, 4)
    component_age = round(random.uniform(0.1, 10), 2)
    temp_cat = get_temp_category(temperature)
    anomaly_score = round(np.random.normal(loc=0, scale=1), 2)
    fault = "Yes" if anomaly_score > 1.8 else "No"

    timestamp = start_time + timedelta(seconds=i)

    data.append([
        timestamp, component, voltage, current, temperature,
        fault, power, component_age, temp_cat, anomaly_score
    ])

# Create DataFrame
columns = [
    "timestamp", "component", "voltage(V)", "current(A)", "temperature(C)",
    "fault", "power(W)", "component_age(years)", "temperature_category", "anomaly_score"
]
df = pd.DataFrame(data, columns=columns)

# Save to CSV
df.to_csv("realistic_circuit_sensor_data.csv", index=False)
print("✅ realistic_circuit_sensor_data.csv with 80,000 rows created.")
