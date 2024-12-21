import paho.mqtt.client as mqtt
from flask import Flask, render_template_string

app = Flask(__name__)

# MQTT server information
server = "xxx.sabanciuniv.edu"
port = 0000
topic = "parking"

# Path to the file where the status will be written
file_path = r'/Volumes/Raamiz SSD/backup/PROJ 201'

# Callback function for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    status = msg.payload.decode('utf-8')
    # Write the status to the file at the specified path
    with open(file_path, 'w') as file:
        file.write(status)

client = mqtt.Client()
client.on_message = on_message

print("Connecting to MQTT server...")
client.connect(server, port, 60)
client.subscribe(topic)
client.loop_start()

@app.route('/get-file-content')
def get_file_content():
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        content = "File not found."
    return content

@app.route('/')
def index():
    return render_template_string("""
        <!DOCTYPE html>
<html>
<head>
    <title>PROJ 201 Parking Sensor</title>
    <style>
        body {
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
            text-align: center;
        }
        .container {
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 50px auto;
            padding: 20px;
            max-width: 400px;
        }
        h1 {
            color: #333;
        }
        .status-box {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            margin: 20px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: bold;
            text-transform: uppercase;
        }
        .parked {
            background-color: #ff5733;
            color: #fff;
        }
        .available {
            background-color: #4caf50;
            color: #fff;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>PROJ 201 Parking Sensor</h1>
        <div class="status-box" id="status-box">Waiting for MQTT messages...</div>
    </div>
    <script>
        function refreshContent() {
            fetch('/get-file-content')
                .then(response => response.text())
                .then(data => {
                    const statusBox = document.getElementById('status-box');
                    if (data === 'parked') {
                        statusBox.className = 'status-box parked';
                        statusBox.innerText = 'Parked';
                    } else if (data === 'available') {
                        statusBox.className = 'status-box available';
                        statusBox.innerText = 'Available';
                    } else {
                        // If the data is neither 'parked' nor 'available', do not change the status box
                    }
                })
                .catch(error => console.error('Error:', error));
        }
        setInterval(refreshContent, 1000); // Refresh every 1000 milliseconds (1 second)
    </script>
</body>
</html>

    """)

if __name__ == '__main__':
    app.run(debug=True)
