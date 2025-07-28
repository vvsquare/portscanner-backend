from flask import Flask, request, jsonify, send_file
from scanner import run_scan
import csv, os
from datetime import datetime

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    ip = data.get('ip')
    ports = list(range(int(data.get('start_port')), int(data.get('end_port')) + 1))
    open_ports = run_scan(ip, ports)

    filename = f"reports/scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Open Ports"])
        for port in open_ports:
            writer.writerow([port])

    return jsonify({
        "open_ports": open_ports,
        "report_url": f"/download?file={filename}"
    })

@app.route('/download')
def download():
    filename = request.args.get("file")
    if os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
