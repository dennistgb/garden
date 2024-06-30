from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import random
import os
from datetime import datetime

app = Flask(__name__)

# File path for the CSV file
csv_file = 'database.csv'

# Function to log data into the CSV file
def log_data(ecval, temp, humidity, phval, light):
    # Get the current timestamp
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    # Create a dictionary for the new entry
    data = {
        'timestamp': [timestamp],
        'EC Level': [ecval],
        'Temperature': [temp],
        'Humidity': [humidity],
        'pH Level': [phval],
        'Light Level': [light]
    }
    
    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)
    
    # Check if the CSV file exists and is not empty
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        # Append the DataFrame to the CSV file
        df.to_csv(csv_file, mode='a', index=False, header=False)
    else:
        # Create the CSV file with the header
        df.to_csv(csv_file, mode='w', index=False, header=True)

# Function to read the data from the CSV file into a DataFrame
def read_data():
    # Check if the CSV file exists and is not empty
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)
        return df
    else:
        # Return an empty DataFrame if the file does not exist or is empty
        return pd.DataFrame(columns=['timestamp', 'EC Level', 'Temperature', 'Humidity', 'pH Level', 'Light Level'])

# Function to analyze data using NumPy
def analyze_data(df):
    analysis = {}
    columns = ['EC Level', 'Temperature', 'Humidity', 'pH Level', 'Light Level']
    
    for col in columns:
        data = df[col].values
        analysis[col] = {
            'mean': np.mean(data),
            'median': np.median(data),
            'std_dev': np.std(data)
        }
    
    return analysis

# Global data storage for real-time simulation
data_storage = {
    "time": [datetime.now().strftime('%Y-%m-%d %H:%M:%S') for _ in range(10)],
    "ph": [random.uniform(5.5, 7.5) for _ in range(10)],
    "temperature": [random.uniform(18, 30) for _ in range(10)],
    "humidity": [random.uniform(30, 70) for _ in range(10)],
    "light": [random.uniform(200, 800) for _ in range(10)],
    "ec": [random.uniform(1.0, 2.5) for _ in range(10)]
}

def update_data():
    current_time = datetime.now().strftime('%H:%M:%S')
    data_storage["time"].append(current_time)
    data_storage["time"].pop(0)
    
    data_storage["ph"].append(random.uniform(5.5, 7.5))
    data_storage["ph"].pop(0)
    
    data_storage["temperature"].append(random.uniform(18, 30))
    data_storage["temperature"].pop(0)
    
    data_storage["humidity"].append(random.uniform(30, 70))
    data_storage["humidity"].pop(0)
    
    data_storage["light"].append(random.uniform(200, 800))
    data_storage["light"].pop(0)
    
    data_storage["ec"].append(random.uniform(1.0, 2.5))
    data_storage["ec"].pop(0)

    # Log the updated data to CSV
    log_data(data_storage["ec"][-1], data_storage["temperature"][-1], data_storage["humidity"][-1], data_storage["ph"][-1], data_storage["light"][-1])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/data')
def data():
    update_data()
    return jsonify(data_storage)

@app.route('/analysis/<metric>')
def analysis(metric):
    df = read_data()
    analysis_result = analyze_data(df)
    if metric in analysis_result:
        return jsonify(analysis_result[metric])
    else:
        return jsonify({"error": "Invalid metric"}), 400

if __name__ == '__main__':
    app.run(debug=True)
