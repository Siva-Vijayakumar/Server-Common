import subprocess
import json
import os

os.makedirs("reports", exist_ok=True)


def run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    output = result.stdout.strip()

    if not output:
        output = "NOT_FOUND"

    return output


report = {}

# --------------------------------------------------
# SERVER INFORMATION
# --------------------------------------------------

report["hostname"] = run_command("hostname")

report["uptime"] = run_command("uptime -p")

report["kernel"] = run_command("uname -r")

report["os"] = run_command(
    "grep PRETTY_NAME /etc/os-release"
)

# --------------------------------------------------
# CPU
# --------------------------------------------------

report["cpu_usage"] = run_command(
    "top -bn1 | grep Cpu"
)

# --------------------------------------------------
# MEMORY
# --------------------------------------------------

report["memory"] = run_command(
    "free -h"
)

memory_percent = run_command(
    "free | awk '/Mem:/ {print int($3/$2 * 100)}'"
)

report["memory_percent"] = int(memory_percent)

# --------------------------------------------------
# DISK
# --------------------------------------------------

report["disk"] = run_command(
    "df -h /"
)

disk_percent = run_command(
    "df / | awk 'NR==2 {print $5}' | sed 's/%//'"
)

report["disk_percent"] = int(disk_percent)

# --------------------------------------------------
# SERVICES
# --------------------------------------------------

report["mysql"] = run_command(
    "systemctl is-active mysql"
)

report["redis"] = run_command(
    "systemctl is-active redis-server"
)

report["nginx"] = run_command(
    "systemctl is-active nginx"
)

# --------------------------------------------------
# PORTS
# --------------------------------------------------

report["mysql_port"] = run_command(
    "ss -tulnp | grep ':3306 '"
)

report["redis_port"] = run_command(
    "ss -tulnp | grep ':6379 '"
)

report["nginx_port"] = run_command(
    "ss -tulnp | grep ':80 '"
)

# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

issues = []

if report["mysql"] != "active":
    issues.append("MySQL Service Down")

if report["redis"] != "active":
    issues.append("Redis Service Down")

if report["nginx"] != "active":
    issues.append("Nginx Service Down")

if report["memory_percent"] > 90:
    issues.append(
        f"High Memory Usage ({report['memory_percent']}%)"
    )

if report["disk_percent"] > 80:
    issues.append(
        f"High Disk Usage ({report['disk_percent']}%)"
    )

if report["mysql_port"] == "NOT_FOUND":
    issues.append("MySQL Port 3306 Not Listening")

if report["redis_port"] == "NOT_FOUND":
    issues.append("Redis Port 6379 Not Listening")

if report["nginx_port"] == "NOT_FOUND":
    issues.append("Nginx Port 80 Not Listening")

# --------------------------------------------------
# FINAL STATUS
# --------------------------------------------------

if issues:
    report["status"] = "REJECTED"
else:
    report["status"] = "READY FOR APPROVAL"

report["issues"] = issues

# --------------------------------------------------
# SAVE REPORT
# --------------------------------------------------

with open(
    "reports/server_report.json",
    "w"
) as file:

    json.dump(
        report,
        file,
        indent=4
    )

print("Precheck completed successfully")