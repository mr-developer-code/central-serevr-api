from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://nidssecure.netlify.app"}}, supports_credentials=True)

# alert_file_to_read = "client_data/alert.json"
# loadconn_file_to_read = "client_data/loadconn.json"
# progress_file_to_read = "client_data/progress.txt"
# package_file_to_read = "client_data/uninstall_package.txt"

network_load = []
network_load_data = []
loadconn_data = []
connection_list = []
connection_data = []

last_fetch_alert = 0
alert_data = []
alert = {}

@app.route("/api/dashboard-packet-data", methods=["POST"])
def dashboard_packet_data():
    global last_fetch_alert

    data = request.get_json()
    address = data['address']

    if len(alert_data) >= 8:
        alert_data.pop(0)
    
    try :
        with open(f"{address}/alert.json", "r") as f:
            f.seek(last_fetch_alert)
            line = f.readline()
            last_fetch_alert = f.tell()

            try:
                entry = json.loads(line)
                
                alert = {
                    "time": entry.get("time", "N/A"),
                    "source": entry.get("source", "N/A"),
                    "destination": entry.get("destination", "N/A"),
                    "protocol": entry.get("protocol", "N/A"),
                    "size": entry.get("size", "N/A"),
                    "status": entry.get("status", "N/A")
                }
                alert_data.append(alert)
                print(len(alert_data))
                
            except json.JSONDecodeError as e:
                print(e)
    except FileNotFoundError:
        return jsonify({"error": "Alert file not found"}), 500
    
    if alert_data:
        return jsonify(alert_data)
    else:
        return jsonify({"message": "No new alerts yet"}), 204
    
@app.route("/api/dashboard-loadconn-data", methods=["POST"])
def dashboard_loadconn_data():

    data = request.get_json()
    address = data['address']

    try :
        with open(f"{address}/loadconn.json", "r") as f:
            line = f.readline()
            try:
                entry = json.loads(line)
                
                data = {
                    "network_load": entry.get("network_load", "N/A"),
                    "network_traffic_data": entry.get("network_traffic_data", "N/A"),
                    "connections" : entry.get("connections", "N/A"),
                    "connections_data" : entry.get("connections_data", "N/A")
                }
                loadconn_data.append(data)
                
            except json.JSONDecodeError as e:
                print(e)
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 500

    if loadconn_data:
        return jsonify(loadconn_data.pop(0))
    else: 
        return jsonify({"message": "No new record yet"}), 204
    
@app.route('/api/progress', methods=['POST'])
def get_progress():
    data = request.get_json()
    address = data['address']
    try:
        with open (f"{address}/progress.txt", "r") as f:
            line = f.readline()
    except FileNotFoundError:
        line = 0
    return jsonify({'progress': line}), 200

@app.route('/api/check-uninstalled-packages', methods=['POST'])
def check_password_status():

    data = request.get_json()
    address = data['address']

    if os.path.exists(f'{address}/uninstall_package.txt'):
        try:
            with open(f'{address}/uninstall_package.txt', 'r') as f:
                lines = f.readlines()

                with open(f'{address}/uninstall_package.txt', 'w') as f:
                    f.write("clear")

                return jsonify({'status': 'need_installation', 'lines': lines}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    else:
        return jsonify({'status': 'ok', 'message': 'all packages are installed'}), 200

if __name__ == "__main__":
    app.run(debug=True, port=1003)

#--------------------------------------------------------------------------------
