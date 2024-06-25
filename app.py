from flask import Flask, render_template
import matplotlib.pyplot as plt
import io
import base64
import random

app = Flask(__name__)

def generate_dummy_data():
    data = {
        "ph": [random.uniform(5.5, 7.5) for _ in range(10)],
        "temperature": [random.uniform(18, 30) for _ in range(10)],
        "humidity": [random.uniform(30, 70) for _ in range(10)],
        "light": [random.uniform(200, 800) for _ in range(10)],
        "ec": [random.uniform(1.0, 2.5) for _ in range(10)]
    }
    return data

def create_graph(data, title, y_label):
    plt.figure()
    plt.plot(data)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel('Time')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return string.decode('utf-8')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    data = generate_dummy_data()
    graphs = {
        "ph": create_graph(data['ph'], 'pH Level', 'pH'),
        "temperature": create_graph(data['temperature'], 'Ambient Temperature', 'Temperature (°C)'),
        "humidity": create_graph(data['humidity'], 'Relative Humidity', 'Humidity (%)'),
        "light": create_graph(data['light'], 'Ambient Light Intensity', 'Light (lux)'),
        "ec": create_graph(data['ec'], 'EC Level', 'EC (mS/cm)')
    }
    return render_template('dashboard.html', graphs=graphs)

if __name__ == '__main__':
    app.run(debug=True)
