from flask import Flask, render_template, jsonify, request, send_file, url_for, session, redirect
import pandas as pd
import os
import json
from functools import wraps

app = Flask(__name__, static_folder='static')
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key in production
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('data', exist_ok=True)

# Context processor to pass auth status to all templates
@app.context_processor
def inject_auth_status():
    return {
        'is_authenticated': 'user' in session,
        'current_user': session.get('user')
    }

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Configuration
UPLOAD_FOLDER = 'data'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/data-upload')
@login_required
def data_upload():
    return render_template('data_upload.html')

@app.route('/mapreduce')
@login_required
def mapreduce():
    return render_template('mapreduce.html')

@app.route('/spark-analysis')
@login_required
def spark_analysis():
    return render_template('spark_analysis.html')

@app.route('/visualizations')
@login_required
def visualizations():
    return render_template('visualizations.html')

@app.route('/components')
@login_required
def components():
    return render_template('components.html')

@app.route('/test-images')
@login_required
def test_images():
    return render_template('test_images.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to home
    if 'user' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/api/login', methods=['POST'])
def api_login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember')

    # TODO: In a real application, validate credentials against a database
    # For demonstration, we'll accept any non-empty email/password
    if email and password:
        session['user'] = email
        if remember:
            session.permanent = True
        return jsonify({
            'status': 'success',
            'message': 'Login successful!',
            'redirect': url_for('index')
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid credentials'
        }), 401

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Process the uploaded data
        try:
            # Read the uploaded CSV file
            df = pd.read_csv(filepath)
            
            # Generate MapReduce results (fault count by component)
            fault_counts = df[df['fault'] == 'Yes'].groupby('component').size().reset_index(name='fault_count')
            fault_counts.to_csv('data/mapreduce_results.csv', index=False)
            
            # Generate Spark analysis results
            # 1. Fault Analysis
            fault_analysis = df[df['fault'] == 'Yes'].groupby('component').agg({
                'voltage(V)': ['mean', 'std'],
                'current(A)': ['mean', 'std'],
                'temperature(C)': ['mean', 'std']
            }).reset_index()
            fault_analysis.columns = ['component', 'avg_voltage', 'std_voltage', 
                                    'avg_current', 'std_current', 
                                    'avg_temperature', 'std_temperature']
            fault_analysis.to_csv('data/spark_fault_analysis.csv', index=False)
            
            # 2. Component Stats
            component_stats = df.groupby('component').agg({
                'voltage(V)': ['mean', 'std', 'min', 'max'],
                'current(A)': ['mean', 'std', 'min', 'max'],
                'temperature(C)': ['mean', 'std', 'min', 'max'],
                'fault': lambda x: (x == 'Yes').sum()
            }).reset_index()
            component_stats.columns = ['component', 'avg_voltage', 'std_voltage', 'min_voltage', 'max_voltage',
                                    'avg_current', 'std_current', 'min_current', 'max_current',
                                    'avg_temperature', 'std_temperature', 'min_temperature', 'max_temperature',
                                    'fault_count']
            component_stats.to_csv('data/spark_component_stats.csv', index=False)
            
            # 3. Power Analysis
            power_analysis = df.groupby('component').agg({
                'power(W)': ['mean', 'std', 'min', 'max']
            }).reset_index()
            power_analysis.columns = ['component', 'avg_power', 'std_power', 'min_power', 'max_power']
            power_analysis.to_csv('data/spark_power_analysis.csv', index=False)
            
            # 4. Temperature Analysis
            temp_analysis = df.groupby('temperature_category').agg({
                'component': 'count',
                'fault': lambda x: (x == 'Yes').sum()
            }).reset_index()
            temp_analysis.columns = ['temperature_category', 'total_count', 'fault_count']
            temp_analysis.to_csv('data/spark_temp_analysis.csv', index=False)
            
            # 5. Hourly Analysis
            df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
            hourly_analysis = df.groupby('hour').agg({
                'fault': lambda x: (x == 'Yes').sum(),
                'component': 'count'
            }).reset_index()
            hourly_analysis.columns = ['hour', 'fault_count', 'total_count']
            hourly_analysis.to_csv('data/spark_hourly_analysis.csv', index=False)
            
            return jsonify({
                'message': 'File uploaded and processed successfully',
                'filepath': filepath
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid file type. Please upload a CSV file.'}), 400

@app.route('/api/mapreduce-results')
def get_mapreduce_results():
    try:
        # Read the fault analysis data
        fault_analysis = pd.read_csv('data/mapreduce_results.csv')
        
        # Read power analysis data
        power_analysis = pd.read_csv('data/spark_power_analysis.csv')
        
        # Read temperature analysis data
        temp_analysis = pd.read_csv('data/spark_component_stats.csv')
        
        # Format the data for the frontend
        response_data = {
            'fault_analysis': fault_analysis.rename(columns={
                'component': 'component_id',
                'fault_count': 'fault_count'
            }).to_dict(orient='records'),
            
            'power_analysis': power_analysis.rename(columns={
                'component': 'component_id',
                'avg_power': 'avg_power',
                'max_power': 'max_power'
            }).to_dict(orient='records'),
            
            'temp_analysis': temp_analysis.rename(columns={
                'component': 'component_id',
                'avg_temperature': 'avg_temp',
                'max_temperature': 'max_temp'
            }).to_dict(orient='records')
        }
        
        return jsonify(response_data)
    except FileNotFoundError:
        # Create dummy data if files not found
        dummy_data = {
            'fault_analysis': [
                {'component_id': 'Resistor', 'fault_count': 10},
                {'component_id': 'Capacitor', 'fault_count': 5},
                {'component_id': 'IC', 'fault_count': 8},
                {'component_id': 'Power Module', 'fault_count': 3}
            ],
            'power_analysis': [
                {'component_id': 'Resistor', 'avg_power': 2.5, 'max_power': 5.0},
                {'component_id': 'Capacitor', 'avg_power': 3.0, 'max_power': 6.0},
                {'component_id': 'IC', 'avg_power': 4.0, 'max_power': 8.0},
                {'component_id': 'Power Module', 'avg_power': 5.0, 'max_power': 10.0}
            ],
            'temp_analysis': [
                {'component_id': 'Resistor', 'avg_temp': 45.0, 'max_temp': 75.0},
                {'component_id': 'Capacitor', 'avg_temp': 50.0, 'max_temp': 80.0},
                {'component_id': 'IC', 'avg_temp': 55.0, 'max_temp': 85.0},
                {'component_id': 'Power Module', 'avg_temp': 60.0, 'max_temp': 90.0}
            ]
        }
        return jsonify(dummy_data)

@app.route('/api/spark-results')
def get_spark_results():
    results = {}
    try:
        # Assuming spark analysis results are in CSV files in the data directory
        results['fault_analysis'] = pd.read_csv('data/spark_fault_analysis.csv').to_dict(orient='records')
        results['component_stats'] = pd.read_csv('data/spark_component_stats.csv').to_dict(orient='records')
        results['power_analysis'] = pd.read_csv('data/spark_power_analysis.csv').to_dict(orient='records')
        results['temp_analysis'] = pd.read_csv('data/spark_temp_analysis.csv').to_dict(orient='records')
        results['hourly_analysis'] = pd.read_csv('data/spark_hourly_analysis.csv').to_dict(orient='records')
        return jsonify(results)
    except FileNotFoundError as e:
        return jsonify({'error': f'Data file not found: {e}'}), 500

@app.route('/api/login-status')
def login_status():
    if 'user' in session:
        return jsonify({
            'logged_in': True,
            'user': session['user'],
            'redirect': url_for('index')
        })
    return jsonify({
        'logged_in': False
    })

@app.route('/register')
def register():
    # If user is already logged in, redirect to home
    if 'user' in session:
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    # TODO: In a real application, you would:
    # 1. Validate the input
    # 2. Check if the email is already registered
    # 3. Hash the password
    # 4. Store the user in a database
    
    # For demonstration, we'll just print the registration attempt
    print(f"Registration attempt: Name - {name}, Email - {email}")

    # Simulate successful registration
    return jsonify({
        'status': 'success',
        'message': 'Registration successful! Please login.',
        'redirect': url_for('login')
    })

# Helper function to get static file path
# @app.context_processor
# def utility_processor():
#     def static_file(filename):
#         return url_for('static', filename=filename)
#     return dict(static_file=static_file)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5004))
    app.run(debug=True, host='0.0.0.0', port=port) 