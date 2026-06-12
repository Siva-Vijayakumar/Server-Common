# import json
# import os
# import requests

# CLIQ_WEBHOOK = os.getenv(
#     "CLIQ_WEBHOOK"
# )

# with open(
#     "reports/server_report.json"
# ) as file:

#     data = json.load(file)

# status_icon = (
#     "✅"
#     if data["status"] == "READY FOR APPROVAL"
#     else "❌"
# )

# issues_text = "None"

# if data["issues"]:
#     issues_text = "\n".join(
#         f"• {issue}"
#         for issue in data["issues"]
#     )

# message = f"""
# 🚀 ServerCommon Health Report

# Hostname:
# {data['hostname']}

# OS:
# {data['os']}

# Kernel:
# {data['kernel']}

# Uptime:
# {data['uptime']}

# ----------------------------------

# Services

# MySQL : {data['mysql']}
# Redis : {data['redis']}
# Nginx : {data['nginx']}

# ----------------------------------

# Memory Usage :
# {data['memory_percent']}%

# Disk Usage :
# {data['disk_percent']}%

# ----------------------------------

# Issues

# {issues_text}

# ----------------------------------

# Status

# {status_icon} {data['status']}
# """

# response = requests.post(
#     CLIQ_WEBHOOK,
#     json={
#         "text": message
#     }
# )

# print(
#     "Cliq Response:",
#     response.status_code
# )


import json
import os
import requests

CLIQ_WEBHOOK = os.getenv("CLIQ_WEBHOOK")

with open("reports/server_report.json") as file:
    data = json.load(file)

status_icon = (
    "✅"
    if data["status"] == "READY FOR APPROVAL"
    else "❌"
)

mysql_icon = (
    "✅"
    if data["mysql"] == "active"
    else "❌"
)

redis_icon = (
    "✅"
    if data["redis"] == "active"
    else "❌"
)

nginx_icon = (
    "✅"
    if data["nginx"] == "active"
    else "❌"
)

issues_text = "None"

if data["issues"]:
    issues_text = "\n".join(
        f"• {issue}"
        for issue in data["issues"]
    )

message = f"""
 *SERVERCOMMON PRECHECK REPORT*

══════════════════════════════════

🖥️ *SERVER DETAILS*

   Hostname  :  `{data['hostname']}`
   OS        :  `{data['os'].replace('PRETTY_NAME=', '').replace('"', '')}`
   Kernel    :  `{data['kernel']}`
   Uptime    :  `{data['uptime']}`

══════════════════════════════════

⚙️ *SERVICE HEALTH*

   {mysql_icon} MySQL     :  *{data['mysql']}*
   {redis_icon} Redis     :  *{data['redis']}*
   {nginx_icon} Nginx     :  *{data['nginx']}*

══════════════════════════════════

📊 *RESOURCE UTILIZATION*

   🧠 Memory Usage :  *{data['memory_percent']}%*
   💾 Disk Usage   :  *{data['disk_percent']}%*

══════════════════════════════════

🚨 *OBSERVATIONS*

{issues_text if issues_text != "None" else "   ✅ No Issues Detected"}

══════════════════════════════════

🎯 *APPROVAL DECISION*

        {status_icon} *{data['status']}*

"""

payload = {
    "text": message,
    "bot": {
        "name": "Server Common"
    },
    "buttons": [
        {
            "label": "Approve",
            "type": "+",
            "action": {
                "type": "open.url",
                "data": {
                    "web": "https://cliq.zoho.in"
                }
            }
        },
        {
            "label": "Reject",
            "type": "-",
            "action": {
                "type": "open.url",
                "data": {
                    "web": "https://cliq.zoho.in"
                }
            }
        }
    ]
}

response = requests.post(
    CLIQ_WEBHOOK,
    json=payload
)

print(
    "Cliq Response:",
    response.status_code
)

print(
    response.text
)