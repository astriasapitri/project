const socket = io();

socket.on('sensor_update', (data) => {
    document.getElementById('temp').innerText = data.temperature ?? '-';
    document.getElementById('hr').innerText = data.heart_rate ?? '-';
    document.getElementById('spo2').innerText = data.spo2 ?? '-';
    document.getElementById('ts').innerText = data.timestamp ?? '-';
});
