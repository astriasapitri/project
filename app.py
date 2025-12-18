import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# SocketIO
socketio = SocketIO(
    app,
    cors_allowed_origins='*',
    async_mode='eventlet'
)

# Data sensor terbaru (sementara / demo)
latest = {
    'temperature': None,
    'heart_rate': None,
    'spo2': None,
    'timestamp': None
}

# ================= ROUTES =================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# ================= API SENSOR (RASPBERRY PI) =================

@app.route('/api/sensor', methods=['POST'])
def sensor_api():
    api_key = request.headers.get('X-API-KEY') or request.args.get('api_key')

    if api_key != app.config['SENSOR_API_KEY']:
        return jsonify({'error': 'unauthorized'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'error': 'no json'}), 400

    latest['temperature'] = data.get('temperature')
    latest['heart_rate']  = data.get('heart_rate')
    latest['spo2']        = data.get('spo2')
    latest['timestamp']   = data.get('timestamp')

    socketio.emit('sensor_update', latest)

    return jsonify({'status': 'success'}), 200


# ================= SOCKET.IO =================

@socketio.on('connect')
def handle_connect():
    emit('sensor_update', latest)


# ================= RUN =================

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
