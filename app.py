from flask import Flask, render_template, jsonify, send_file
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg'
import matplotlib.pyplot as plt
import io
import random

app = Flask(__name__)

# Dummy sensor data for demonstration
def get_sensor_data():
    return {
        'ph': round(random.uniform(5.5, 6.5), 2),
        'temperature': round(random.uniform(20.0, 25.0), 1),
        'humidity': round(random.uniform(50.0, 70.0), 1),
        'light': round(random.uniform(200, 800), 1),
        'ec': round(random.uniform(1.2, 2.0), 2)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sensor_data')
def sensor_data():
    data = get_sensor_data()
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
    # Generate some dummy data for the graph
    data = [get_sensor_data()[sensor_type] for _ in range(10)]
    ylabel_map = {
        'ph': 'pH Level',
        'temperature': 'Temperature (°C)',
        'humidity': 'Humidity (%)',
        'light': 'Light Intensity (lx)',
        'ec': 'EC Level'
    }
    graph = create_graph(data, sensor_type.capitalize(), ylabel_map[sensor_type])
    return send_file(graph, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
