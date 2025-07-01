# Spark Analysis Integration Guide

## Overview

This document describes the integration of Spark analysis results into the Circuit Dashboard web application. The integration provides interactive visualizations of circuit component analysis using Apache Spark, with download capabilities for various formats.

## What Was Implemented

### 1. Backend Integration (Flask App)

**File Modified:** `circuit_dashboard/app.py`

**New Route:** `/api/spark-results`

- Reads CSV files from `spark_analysis_module/results/` directory
- Handles different CSV formats (with and without headers)
- Returns JSON data for frontend consumption
- Includes session validation for uploaded datasets

**CSV Files Supported:**
- `faults.csv` - Fault frequency by component
- `power.csv` - Average power consumption by component  
- `temp.csv` - Average temperature by category
- `anomaly.csv` - Hourly anomaly score trend

### 2. Frontend Integration (HTML Template)

**File Modified:** `circuit_dashboard/templates/spark_analysis.html`

**New Features:**
- Interactive Plotly charts for all four analysis types
- Download functionality for CSV, PDF, Excel, and PNG formats
- Responsive design with modern UI
- Real-time data loading from Spark analysis results

**Charts Implemented:**
1. **Fault Frequency Bar Chart** - Shows fault count by component
2. **Power Consumption Pie Chart** - Shows average power by component
3. **Temperature Bar Chart** - Shows average temperature by category
4. **Anomaly Score Line Chart** - Shows hourly anomaly trend

## How to Use

### 1. Running the Application

```bash
cd circuit_dashboard
python app.py
```

The application will run on `http://localhost:5004`

### 2. Accessing Spark Analysis Results

1. **Login** to the application
2. **Upload a dataset** via the Data Upload page
3. **Navigate** to "Spark Analysis" in the navigation menu
4. **View** the interactive charts and analysis results
5. **Download** results in various formats using the download buttons

### 3. Triggering New Spark Analysis

To update the dashboard with new analysis results:

1. **Run Spark Analysis:**
   ```bash
   python spark_analysis.py
   ```
   This will update the CSV files in `spark_analysis_module/results/`

2. **Refresh the Dashboard:**
   - The dashboard automatically reads the latest CSV files
   - No manual refresh needed - data is loaded dynamically

### 4. Download Options

- **CSV Download:** Downloads all analysis results as a single CSV file
- **PDF Report:** Placeholder for comprehensive PDF report generation
- **Excel Download:** Placeholder for multi-sheet Excel file
- **PNG Images:** Downloads each chart as a high-resolution PNG image

## Technical Details

### Data Flow

```
Spark Analysis Script → CSV Files → Flask API → Frontend Charts
```

1. **Spark Analysis** (`spark_analysis.py`) processes data and creates CSV files
2. **Flask API** (`/api/spark-results`) reads CSV files and serves JSON
3. **Frontend** loads JSON data and renders interactive Plotly charts

### CSV File Formats

#### faults.csv
```csv
component,fault_count
Buck Converter,178
Thick Film Resistor,178
...
```

#### power.csv
```csv
component,avg_power_W
Rheostat,13.512246510020747
Inverter Module,13.19613305766139
...
```

#### temp.csv
```csv
temperature_category,avg_temp_C
High,79.59481585832134
Normal,54.966237963422834
Low,34.77158752327749
```

#### anomaly.csv
```csv
hour,avg_anomaly_score
0,0.01064444444444446
1,-0.005761111111110977
...
```

### Chart Specifications

| Chart Type | Data Source | Visualization | Interactivity |
|------------|-------------|---------------|---------------|
| Fault Frequency | faults.csv | Bar Chart | Hover, Zoom, Pan |
| Power Consumption | power.csv | Pie Chart | Hover, Click |
| Temperature | temp.csv | Bar Chart | Hover, Zoom, Pan |
| Anomaly Trend | anomaly.csv | Line Chart | Hover, Zoom, Pan |

## Troubleshooting

### Common Issues

1. **"No results available" Error**
   - Ensure you have uploaded a dataset first
   - Check that CSV files exist in `spark_analysis_module/results/`

2. **Charts Not Loading**
   - Check browser console for JavaScript errors
   - Verify Plotly library is loading correctly
   - Ensure API endpoint is accessible

3. **CSV Reading Errors**
   - Verify CSV file formats match expected structure
   - Check file permissions and paths

### Debug Mode

To enable debug logging, set Flask debug mode:

```python
app.run(debug=True, host='0.0.0.0', port=5004)
```

## Future Enhancements

### Planned Features

1. **PDF Report Generation**
   - Implement comprehensive PDF reports with charts and analysis
   - Use libraries like ReportLab or WeasyPrint

2. **Excel Export**
   - Create multi-sheet Excel files with all analysis results
   - Include formatted charts and data tables

3. **Real-time Updates**
   - WebSocket integration for live data updates
   - Automatic chart refresh when new analysis completes

4. **Advanced Filtering**
   - Date range filters
   - Component type filters
   - Threshold-based filtering

### Code Extensions

To add new analysis types:

1. **Add CSV file** to `spark_analysis_module/results/`
2. **Update Flask API** to read the new file
3. **Add chart function** in the frontend JavaScript
4. **Update download functions** to include new data

## Dependencies

### Required Python Packages
```
Flask==3.0.2
pandas==2.2.1
numpy==1.26.4
pyspark==3.5.1
```

### Frontend Libraries
```
Plotly.js (CDN)
Tailwind CSS (already included)
```

## Testing

Run the integration test:

```bash
python test_spark_integration.py
```

This will verify:
- CSV file accessibility
- Data parsing correctness
- JSON serialization
- File structure validation

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review browser console for JavaScript errors
3. Verify CSV file formats and paths
4. Test with the provided integration test script 