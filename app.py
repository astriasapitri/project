import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

socketio = SocketIO(
    app,
    cors_allowed_origins='*',
    async_mode='eventlet'
)

latest = {
    'temperature': None,
    'heart_rate': None,
    'spo2': None,
    'timestamp': None,
    'status_text': None,
    'status_level': None
}

def classify(latest):
    hr = latest.get("heart_rate")
    spo2 = latest.get("spo2")

    status = "Tidak ada data"
    level = "unknown"

    # SpO2 priority
    if spo2 is not None:
        try:
            spo2_val = float(spo2)
            if spo2_val >= 95:
                status = "SpO₂ Normal"
                level = "normal"
            elif 90 <= spo2_val < 95:
                status = "SpO₂ Waspada"
                level = "warn"
            else:
                status = "SpO₂ Bahaya"
                level = "danger"
        except (ValueError, TypeError):
            status = "SpO₂ tidak valid"
            level = "unknown"

    # HR only if realistic BPM
    if hr is not None:
        try:
            hr_val = float(hr)
            if 30 <= hr_val <= 220:
                if hr_val < 60:
                    status += " | HR Rendah"
                elif hr_val <= 100:
                    status += " | HR Normal"
                else:
                    status += " | HR Tinggi"
        except (ValueError, TypeError):
            pass

    return status, level

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/sensor', methods=['POST'])
def sensor_api():
    api_key = request.headers.get('X-API-KEY') or request.args.get('api_key')
    if api_key != app.config['SENSOR_API_KEY']:
        return jsonify({'error': 'unauthorized'}), 401

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'no json'}), 400

    latest['temperature'] = data.get('temperature')
    latest['heart_rate']  = data.get('heart_rate')
    latest['spo2']        = data.get('spo2')
    latest['timestamp']   = data.get('timestamp')

    # ✅ hitung status SETIAP data masuk
    latest["status_text"], latest["status_level"] = classify(latest)

    socketio.emit('sensor_update', latest)
    return jsonify({'status': 'success'}), 200

@socketio.on('connect')
def handle_connect():
    # ✅ biar pas reload dashboard juga ada status
    latest["status_text"], latest["status_level"] = classify(latest)
    emit('sensor_update', latest)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
