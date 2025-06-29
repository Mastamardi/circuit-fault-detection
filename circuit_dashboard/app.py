from flask import Flask, render_template, jsonify, request, send_file, url_for, session, redirect
import pandas as pd
import os
import json
from functools import wraps
import glob
import subprocess
import threading
import shutil

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
    session.pop('uploaded', None)  # Clear upload flag on logout
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
        # Clear any existing analysis flags to ensure clean state
        session.pop('uploaded', None)
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
        # Clear previous results and cache
        for old_file in glob.glob('data/*.csv'):
            try:
                os.remove(old_file)
            except:
                pass
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        session['uploaded'] = True  # Set session flag immediately
        
        # Pandas-based validation and notification logic
        try:
            df = pd.read_csv(filepath)
            required_columns = ['component', 'voltage(V)', 'current(A)', 'temperature(C)', 'power(W)', 'fault', 'timestamp']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return jsonify({'error': f'Invalid dataset. Missing required columns: {missing_columns}'}), 400
            if df.empty:
                return jsonify({'error': 'Dataset is empty. Please upload a valid dataset.'}), 400
            total_records = int(len(df))
            unique_components = int(df['component'].nunique())
            total_faults = int((df['fault'] == 'Yes').sum())
        except Exception as e:
            return jsonify({'error': f'Error validating file: {str(e)}'}), 400
        
        # Run MapReduce and Spark analysis as background steps (non-blocking)
        try:
            def run_analysis():
                try:
                    # Copy uploaded file to expected name for MapReduce scripts
                    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    shutil.copy(filepath, os.path.join(parent_dir, 'realistic_circuit_sensor_data.csv'))

                    print("Running mapreduce_fault_analysis.py...")
                    subprocess.run(['python3', os.path.join(parent_dir, 'mapreduce_fault_analysis.py')], check=True, cwd=parent_dir)
                    if os.path.exists(os.path.join(os.path.dirname(__file__), 'data', 'fault_analysis_results.csv')):
                        print("Fault analysis done.")

                    print("Running mapreduce_avg_power.py...")
                    subprocess.run(['python3', os.path.join(parent_dir, 'mapreduce_avg_power.py')], check=True, cwd=parent_dir)
                    if os.path.exists(os.path.join(os.path.dirname(__file__), 'data', 'power_analysis_results.csv')):
                        print("Power analysis done.")

                    print("Running mapreduce_temp_behavior.py...")
                    subprocess.run(['python3', os.path.join(parent_dir, 'mapreduce_temp_behavior.py')], check=True, cwd=parent_dir)
                    if os.path.exists(os.path.join(os.path.dirname(__file__), 'data', 'temperature_analysis_results.csv')):
                        print("Temperature analysis done.")

                    print("Running spark_analysis.py...")
                    try:
                        spark_result = subprocess.run(['python3', os.path.join(parent_dir, 'spark_analysis.py'), filepath], 
                                                    check=True, cwd=parent_dir, capture_output=True, text=True)
                        print("Spark analysis completed successfully.")
                        print("Spark output:", spark_result.stdout)
                    except subprocess.CalledProcessError as e:
                        print(f"Spark analysis failed with error: {e}")
                        print(f"Spark error output: {e.stderr}")
                    except Exception as e:
                        print(f"Spark analysis exception: {e}")
                    
                    # Move Spark output files to expected locations
                    print("Moving Spark output files...")
                    move_spark_outputs()
                    print("Analysis complete - all files processed")
                except Exception as e:
                    print(f"Analysis error: {e}")
            threading.Thread(target=run_analysis).start()
        except Exception as e:
            print(f"Error starting analysis thread: {e}")

        # Always return a response after starting the thread
        return jsonify({
            'message': 'File uploaded and processing started successfully',
            'filepath': filepath,
            'dataset_info': {
                'total_records': total_records,
                'components': unique_components,
                'fault_count': total_faults
            }
        }), 200
    else:
        return jsonify({'error': 'Invalid file type. Please upload a CSV file.'}), 400

@app.route('/api/mapreduce-results')
def get_mapreduce_results():
    # Check if user has uploaded a dataset
    if not session.get('uploaded'):
        return jsonify({'error': 'No results available. Please upload a dataset first.'}), 404
    try:
        response_data = {}
        missing_files = []
        
        analysis_files = {
            'fault_analysis': ('data/fault_analysis_results.csv', {
                'Component': 'component_id',
                'Fault_Count': 'fault_count',
                'Fault_Percentage': 'fault_percentage'
            }),
            'power_analysis': ('data/power_analysis_results.csv', {
                'Component': 'component_id',
                'Average_Power_Watts': 'avg_power'
            }),
            'temp_analysis': ('data/temperature_analysis_results.csv', {
                'Temperature_Category': 'component_id',
                'Average_Temperature_C': 'avg_temp'
            })
        }
        
        for key, (filepath, column_mapping) in analysis_files.items():
            abs_path = os.path.abspath(filepath)
            print(f"DEBUG: Checking for {key} at {abs_path}")
            if os.path.exists(filepath):
                try:
                    df = pd.read_csv(filepath)
                    # Add dummy columns for frontend compatibility
                    if key == 'power_analysis':
                        df['max_power'] = df['avg_power'] if 'avg_power' in df.columns else df['Average_Power_Watts']
                    if key == 'temp_analysis':
                        df['max_temp'] = df['avg_temp'] if 'avg_temp' in df.columns else df['Average_Temperature_C']
                    response_data[key] = df.rename(columns=column_mapping).to_dict(orient='records')
                except Exception as e:
                    missing_files.append(f"{key}: {str(e)}")
            else:
                missing_files.append(f"{key}: file not found at {abs_path}")
        
        if not response_data:
            return jsonify({'error': f'No analysis results found. Missing files: {missing_files}'}), 404
        
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': f'Error reading analysis results: {str(e)}'}), 500

@app.route('/api/spark-results')
def get_spark_results():
    # Check if user has uploaded a dataset
    if not session.get('uploaded'):
        return jsonify({'error': 'No results available. Please upload a dataset first.'}), 404
    results = {}
    missing_files = []
    
    try:
        # Get the absolute path to the data directory
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        
        # Try to read each Spark analysis result file
        spark_files = {
            'fault_analysis': os.path.join(data_dir, 'spark_fault_analysis.csv'),
            'component_stats': os.path.join(data_dir, 'spark_component_stats.csv'), 
            'power_analysis': os.path.join(data_dir, 'spark_power_analysis.csv'),
            'temp_analysis': os.path.join(data_dir, 'spark_temp_analysis.csv'),
            'hourly_analysis': os.path.join(data_dir, 'spark_hourly_analysis.csv'),
            'fault_stats': os.path.join(data_dir, 'spark_fault_stats.csv'),
            'component_summary': os.path.join(data_dir, 'component_summary.csv'),
            'temperature_trends': os.path.join(data_dir, 'temperature_trends.csv'),
            'time_trend': os.path.join(data_dir, 'time_trend.csv'),
            'correlation_matrix': os.path.join(data_dir, 'correlation_matrix.csv'),
            'heat_analysis': os.path.join(data_dir, 'heat_analysis.csv')
        }
        
        for key, filepath in spark_files.items():
            if os.path.exists(filepath):
                try:
                    df = pd.read_csv(filepath)
                    results[key] = df.to_dict(orient='records')
                except Exception as e:
                    missing_files.append(f"{key}: {str(e)}")
            else:
                missing_files.append(f"{key}: file not found")
        
        if not results:
            # Only return session error if no files exist AND no session
            if not session.get('uploaded'):
                return jsonify({'error': 'No results available. Please upload a dataset first.'}), 404
            else:
                return jsonify({'error': f'No Spark results found. Missing files: {missing_files}'}), 404
            
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': f'Error reading Spark results: {str(e)}'}), 500

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

# Function to move Spark output part files to single CSV files
def move_spark_outputs():
    """Flatten all Spark output directories in data/ to single CSV files"""
    import shutil
    try:
        os.makedirs('data', exist_ok=True)
        # Find all directories in data/ that end with .csv (Spark output dirs)
        for entry in os.listdir('data'):
            dir_path = os.path.join('data', entry)
            if os.path.isdir(dir_path) and entry.endswith('.csv'):
                print(f"Processing Spark output directory: {entry}")
                # The flat file should be data/<dirname>.csv
                flat_file = os.path.join('data', entry)
                
                # Find part-*.csv file
                part_files = [f for f in os.listdir(dir_path) if f.startswith('part-') and f.endswith('.csv')]
                if part_files:
                    part_file = part_files[0]
                    part_file_path = os.path.join(dir_path, part_file)
                    
                    # Create a temporary file first
                    temp_file = flat_file + '.tmp'
                    
                    # Copy the part file to the temporary file
                    shutil.copy2(part_file_path, temp_file)
                    print(f"Copied {part_file} to temporary file {temp_file}")
                    
                    # Remove the original part file
                    os.remove(part_file_path)
                    print(f"Removed original part file: {part_file_path}")
                    
                    # Remove the now-empty directory
                    shutil.rmtree(dir_path)
                    print(f"Removed directory: {dir_path}")
                    
                    # If the destination file already exists, remove it
                    if os.path.isfile(flat_file):
                        os.remove(flat_file)
                        print(f"Removed existing file: {flat_file}")
                    
                    # Move the temporary file to the final location
                    shutil.move(temp_file, flat_file)
                    print(f"Moved temporary file to {flat_file}")
                else:
                    print(f"No part-*.csv file found in {dir_path}")
        print("Spark output flattening completed successfully")
    except Exception as e:
        print(f"Error moving Spark outputs: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5004))
    app.run(debug=True, host='0.0.0.0', port=port) 