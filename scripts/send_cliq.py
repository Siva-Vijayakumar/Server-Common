import json
import os
import requests

CLIQ_WEBHOOK = os.getenv(
    "CLIQ_WEBHOOK"
)

with open(
    "reports/server_report.json"
) as file:

    data = json.load(file)

status_icon = (
    "✅"
    if data["status"] == "READY FOR APPROVAL"
    else "❌"
)

issues_text = "None"

if data["issues"]:
    issues_text = "\n".join(
        f"• {issue}"
        for issue in data["issues"]
    )

message = f"""
🚀 ServerCommon Health Report

Hostname:
{data['hostname']}

OS:
{data['os']}

Kernel:
{data['kernel']}

Uptime:
{data['uptime']}

--------------------------------

Services

MySQL :
{data['mysql']}

Redis :
{data['redis']}

SSH :
{data['ssh']}

--------------------------------

Resource Usage

Memory :
{data['memory_percent']}%

Disk :
{data['disk_percent']}%

--------------------------------

Issues

{issues_text}

--------------------------------

Status

{status_icon} {data['status']}
"""

response = requests.post(
    CLIQ_WEBHOOK,
    json={
        "text": message
    }
)

print(
    "Cliq Response:",
    response.status_code
)