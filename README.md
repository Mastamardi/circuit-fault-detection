# Circuit Component Fault Detection Dashboard

## AI Chatbot Name Suggestion

CircuitSense AI

## Project Overview

CircuitSense AI is a comprehensive dashboard and analysis system designed for detecting faults in electronic circuit board components. Leveraging big data processing techniques, the project utilizes Apache Spark and custom MapReduce implementations to analyze large volumes of sensor data.

The system provides a web-based interface for data upload, distributed analysis of component behavior, fault patterns, temperature trends, and power consumption. Visualizations are integrated using libraries like Matplotlib and Seaborn, with potential for advanced analytics via Tableau, to offer actionable insights for maintenance and optimization.

## Key Features

-   **Data Loading and Preprocessing:** Efficient handling of large CSV datasets using PySpark.
-   **Distributed Analysis:** In-depth analysis of component data, faults, temperature, and time-based patterns using Apache Spark.
-   **MapReduce Processing:** Custom MapReduce jobs for detailed fault, temperature, power, and anomaly trend analysis.
-   **Interactive Dashboard:** A Flask-based web interface for data upload, viewing analysis results, and interactive visualizations.
-   **Visualization:** Utilization of libraries like Matplotlib and Seaborn for clear and informative graphical representations.
-   **Responsive Design:** Ensures the dashboard is accessible and user-friendly across various devices.

## Technical Stack

-   Apache Spark (PySpark)
-   Python MapReduce implementation
-   Flask Web Framework
-   Matplotlib/Seaborn
-   Tableau (for potential advanced analytics)
-   CSV Data Storage

## Setup and Installation

*(Provide instructions on how to set up the project, including dependencies and running the Flask app)*

## Usage

*(Explain how to use the dashboard, upload data, and view results)*

## Contributing

*(Optional: Guidelines for contributing to the project)*

## License

*(Specify the project's license)*

## 🚀 Tech Stack

### Frontend
- **HTML5 & CSS3**
  - Tailwind CSS for responsive design
  - Custom CSS animations
  - Dark/Light mode support
- **JavaScript**
  - Chart.js for data visualization
  - AOS (Animate On Scroll) library
  - Custom animations and transitions
- **UI Components**
  - Responsive navigation
  - Interactive cards
  - Dynamic charts
  - File upload interface
  - Dark mode toggle

### Backend
- **Python**
  - Flask web framework
  - PySpark for distributed computing
  - Pandas for data manipulation
- **Data Processing**
  - Apache Spark
  - MapReduce implementation
  - Real-time data analysis
- **API Endpoints**
  - File upload handling
  - Data analysis results
  - MapReduce results
  - Spark analysis results

### Database & Storage
- **Data Storage**
  - CSV file storage
  - Local file system for uploads
- **Data Processing**
  - Distributed computing with Spark
  - Batch processing with MapReduce

### Development Tools
- **Version Control**
  - Git
- **Development Environment**
  - VS Code
  - Python virtual environment
- **Dependencies**
  - Flask==3.0.2
  - pandas==2.2.1
  - numpy==1.26.4
  - pyspark==3.5.1
  - python-dotenv==1.0.1
  - Werkzeug==3.0.1

## 🛠️ Features

### Data Processing
- Real-time circuit board sensor data analysis
- Fault detection and prediction
- Component performance monitoring
- Temperature analysis
- Power consumption tracking

### Visualization
- Interactive charts and graphs
- Component statistics
- Fault distribution analysis
- Temperature trends
- Power consumption patterns

### User Interface
- Responsive design
- Dark/Light mode
- Interactive dashboard
- File upload system
- Real-time data updates

## 📊 Data Fields

The system processes the following sensor data:
- Timestamp
- Component type
- Voltage (V)
- Current (A)
- Temperature (C)
- Fault status
- Power consumption (W)
- Component age
- Temperature category
- Anomaly score

## 🏗️ Project Structure
```
circuit_dashboard/
├── app.py                 # Main Flask application
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   └── ...
├── static/              # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── data/               # Data storage
└── uploads/           # File upload directory
```

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone [repository-url]
   cd circuit_dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the dashboard**
   - Open your browser
   - Visit `http://127.0.0.1:5004`

## 👥 Team Members
- Omkar Babu Mastamardi (1RV23AI403)
- Sabaasultana Namaji (1RV23AI405)
- Rishikesh Nitin Kakade (1RV22AI045)

## 👨‍🏫 Project Guidance
Under the guidance of Prof. Vijayalakshmi M.N.

## 📝 License
© 2025 Circuit Component Fault Detection Dashboard | RV College of Engineering 