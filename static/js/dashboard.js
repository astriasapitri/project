const socket = io();

// DATA GRAFIK
const labels = [];
const tempData = [];
const hrData = [];
const spo2Data = [];

const ctx = document.getElementById('healthChart').getContext('2d');

const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels,
    datasets: [
      {
        label: 'Suhu (°C)',
        data: tempData,
        borderWidth: 2
      },
      {
        label: 'Detak Jantung',
        data: hrData,
        borderWidth: 2
      },
      {
        label: 'SpO₂ (%)',
        data: spo2Data,
        borderWidth: 2
      }
    ]
  },
  options: {
    responsive: true,
    animation: false
  }
});

// SOCKET UPDATE
socket.on('sensor_update', data => {
  if (!data || !data.timestamp) return;

  // Update kartu
  document.getElementById('temp').textContent = data.temperature;
  document.getElementById('hr').textContent   = data.heart_rate;
  document.getElementById('spo2').textContent = data.spo2;
  document.getElementById('ts').textContent   = data.timestamp;

  // Update grafik (max 10 data)
  labels.push(data.timestamp);
  tempData.push(data.temperature);
  hrData.push(data.heart_rate);
  spo2Data.push(data.spo2);

  if (labels.length > 10) {
    labels.shift();
    tempData.shift();
    hrData.shift();
    spo2Data.shift();
  }

  chart.update();
});
