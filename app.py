from flask import Flask, render_template, jsonify, send_file, request, redirect, url_for, flash
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg'
import matplotlib.pyplot as plt
import io
import random
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ph REAL,
                    temperature REAL,
                    humidity REAL,
                    light REAL,
                    ec REAL
                )''')
    conn.commit()
    conn.close()

# Dummy sensor data for demonstration
def get_sensor_data():
    return {
        'ph': round(random.uniform(5.5, 6.5), 2),
        'temperature': round(random.uniform(20.0, 25.0), 1),
        'humidity': round(random.uniform(50.0, 70.0), 1),
        'light': round(random.uniform(200, 800), 1),
        'ec': round(random.uniform(1.2, 2.0), 2)
    }

def store_sensor_data(data):
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO sensor_data (ph, temperature, humidity, light, ec) VALUES (?, ?, ?, ?, ?)",
              (data['ph'], data['temperature'], data['humidity'], data['light'], data['ec']))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sensor_data')
def sensor_data():
    data = get_sensor_data()
    store_sensor_data(data)
    return jsonify(data)

def create_graph(data, label, ylabel):
    fig, ax = plt.subplots()
    ax.plot(data, marker='o', linestyle='-')
    ax.set_xlabel('Time')
    ax.set_ylabel(ylabel)
    ax.set_title(f'{label} over Time')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf

@app.route('/graph/<sensor_type>')
def graph(sensor_type):
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    c.execute(f"SELECT {sensor_type} FROM sensor_data ORDER BY timestamp DESC LIMIT 10")
    data = [row[0] for row in c.fetchall()]
    conn.close()

    ylabel_map = {
        'ph': 'pH Level',
        'temperature': 'Temperature (°C)',
        'humidity': 'Humidity (%)',
        'light': 'Light Intensity (lx)',
        'ec': 'EC Level'
    }
    graph = create_graph(data[::-1], sensor_type.capitalize(), ylabel_map[sensor_type])
    return send_file(graph, mimetype='image/png')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        interval = request.form.get('interval')
        # Save settings to a configuration file or database
        flash(f'Settings updated! Interval set to {interval} seconds.')
        return redirect(url_for('settings'))
    return render_template('settings.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
