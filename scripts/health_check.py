import psutil
import socket
import json
import os
import requests

from datetime import datetime

hostname = socket.gethostname()

cpu_usage = psutil.cpu_percent(interval=1)

memory = psutil.virtual_memory()

disk = psutil.disk_usage('/')

report = {
    "hostname": hostname,
    "cpu_usage": f"{cpu_usage}%",
    "memory_usage": f"{memory.percent}%",
    "disk_usage": f"{disk.percent}%",
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

with open("reports/report.json", "w") as f:
    json.dump(report, f, indent=4)

message = f"""
🚀 Server Health Report

Hostname : {report['hostname']}
CPU Usage : {report['cpu_usage']}
Memory Usage : {report['memory_usage']}
Disk Usage : {report['disk_usage']}

Generated At :
{report['timestamp']}

Status :
Awaiting Approval
"""

webhook_url = os.getenv("CLIQ_WEBHOOK")
# webhook_url = "https://cliq.zoho.in/api/v2/channelsbyname/servercommonapproval/message?zapikey=1001.376e44fb7b7898ab9621395e248d3e1d.339ab51536526c8f79f4171f22b2a80c"

if webhook_url:
    requests.post(
        webhook_url,
        json={
            "text": message
        }
    )

print("Report sent successfully")