from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/check-uninstalled-packages', methods=['POST'])
def check_uninstalled_packages():
    received_pack = request.get_json()

    if "install" in received_pack['task']:
        lines = received_pack['lines']
        address = received_pack['address']

        os.makedirs(address,exist_ok=True)
        with open(f"{address}/uninstall_package.txt", "a") as f:
            for line in lines:
                f.write(line)

    return jsonify({'status': 'successful', 'message':"received"}), 200

@app.route('/api/progress', methods=['POST'])
def get_progress():
    received_prog = request.get_json()

    line = received_prog['line']
    address = received_prog['address']

    os.makedirs(address, exist_ok=True)
    with open(f"{address}/progress.txt", "w") as f:
        f.write(str(line))

    print("received")
    return jsonify({'status': 'successful', 'message':"received"}), 200

@app.route("/api/dashboard-loadconn-data", methods=["POST"])
def dashboard_loadconn_data():
    received_lc = request.get_json()

    received_network_load = received_lc['network_load']
    received_network_traffic_data = received_lc['network_traffic_data']
    received_connections = received_lc['connections']
    received_connections_data = received_lc['connections_data']
    address = received_lc['address']

    data = {
        "network_load": received_network_load,
        "network_traffic_data": received_network_traffic_data,
        "connections" : received_connections,
        "connections_data" : received_connections_data
    }

    os.makedirs(address, exist_ok=True)
    with open(f"{address}/loadconn.json", "w") as f:
        f.write(json.dumps(data))

    print("received")
    return jsonify({'status': 'successful', 'message':"received"}), 200

@app.route("/api/adnids-dashboard-packet-data", methods=["POST"])
def adnids_dashboard_packet_data():
    received_an = request.get_json()

    alert_an_list = received_an['alert_list']
    received_message = received_an['message']
    address = received_an['address']

    if "No new alert yet" in received_message:
        print("no new alert")
        return jsonify({'status': 'successful', 'message':"received"}), 200
    if "Alert file not found" in received_message:
        return jsonify({'status': 'successful', 'message':"waiting"}), 200

    os.makedirs(address, exist_ok=True)
    with open(f"{address}/alert.json", "a") as f:
        for alert in alert_an_list:
            f.write(json.dumps(alert) + "\n")

    print("received")
    return jsonify({'status': 'successful', 'message':"received"}), 200

@app.route("/api/dashboard-packet-data", methods=["POST"])
def dashboard_packet_data():
    received_sn = request.get_json()

    alert_sn_list = received_sn['alert_list']
    received_message = received_sn['message']
    address = received_sn['address']

    if "No new alert yet" in received_message:
        print("No new alert")
        return jsonify({'status': 'successful', 'message':"received"}), 200
    if "Alert file not found" in received_message:
        print("waiting")
        return jsonify({'status': 'successful', 'message':"waiting"}), 200
    
    os.makedirs(address, exist_ok=True)
    with open(f"{address}/alert.json", "a") as f:
        print(len(alert_sn_list))
        for alert in alert_sn_list:
            f.write(json.dumps(alert) + "\n")
    print("received")
    return jsonify({'status': 'successful', 'message':"received"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=4358)

#--------------------------------------------------------------------------------