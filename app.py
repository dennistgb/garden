from flask import Flask, render_template, jsonify
import random
import time

app = Flask(__name__)

# Global data storage for real-time simulation
data_storage = {
    "time": list(range(10)),
    "ph": [random.uniform(5.5, 7.5) for _ in range(10)],
    "temperature": [random.uniform(18, 30) for _ in range(10)],
    "humidity": [random.uniform(30, 70) for _ in range(10)],
    "light": [random.uniform(200, 800) for _ in range(10)],
    "ec": [random.uniform(1.0, 2.5) for _ in range(10)]
}

def update_data():
    current_time = data_storage["time"][-1] + 1
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

if __name__ == '__main__':
    app.run(debug=True)
