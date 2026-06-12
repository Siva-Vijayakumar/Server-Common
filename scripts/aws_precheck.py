import paramiko
import os
import json

HOST = os.getenv("EC2_HOST")
USER = os.getenv("EC2_USER")
PRIVATE_KEY = os.getenv("EC2_PRIVATE_KEY")

os.makedirs("reports", exist_ok=True)

with open("temp_key.pem", "w") as key_file:
    key_file.write(PRIVATE_KEY) 

os.chmod("temp_key.pem", 0o600)

key = paramiko.RSAKey.from_private_key_file("temp_key.pem")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(
    hostname=HOST,
    username=USER,
    pkey=key,
    timeout=30
)

commands = {
    "hostname": "hostname",
    "uptime": "uptime -p",
    "os": "grep PRETTY_NAME /etc/os-release",
    "kernel": "uname -r",

    "cpu_usage":
        "top -bn1 | grep Cpu",

    "memory":
        "free -h",

    "disk":
        "df -h /",

    "mysql":
        "systemctl is-active mysql",

    "redis":
        "systemctl is-active redis-server",

    "ssh":
        "systemctl is-active ssh",

    "mysql_port":
        "ss -tulnp | grep ':3306 '",

    "redis_port":
        "ss -tulnp | grep ':6379 '",

    "ssh_port":
        "ss -tulnp | grep ':22 '",

    "mysql_process":
        "pgrep mysqld",

    "redis_process":
        "pgrep redis-server"
}

report = {}

for name, command in commands.items():

    stdin, stdout, stderr = ssh.exec_command(command)

    output = stdout.read().decode().strip()

    if not output:
        output = "NOT_FOUND"

    report[name] = output


# Memory %

stdin, stdout, stderr = ssh.exec_command(
    "free | awk '/Mem:/ {print int($3/$2 * 100)}'"
)

memory_percent = int(
    stdout.read().decode().strip()
)

# Disk %

stdin, stdout, stderr = ssh.exec_command(
    "df / | awk 'NR==2 {print $5}' | sed 's/%//'"
)

disk_percent = int(
    stdout.read().decode().strip()
)

report["memory_percent"] = memory_percent
report["disk_percent"] = disk_percent

issues = []

if memory_percent > 90:
    issues.append(
        f"High Memory Usage ({memory_percent}%)"
    )

if disk_percent > 80:
    issues.append(
        f"High Disk Usage ({disk_percent}%)"
    )

if report["mysql"] != "active":
    issues.append(
        "MySQL Service Down"
    )

if report["redis"] != "active":
    issues.append(
        "Redis Service Down"
    )

if report["ssh"] != "active":
    issues.append(
        "SSH Service Down"
    )

if report["mysql_port"] == "NOT_FOUND":
    issues.append(
        "MySQL Port 3306 Not Listening"
    )

if report["redis_port"] == "NOT_FOUND":
    issues.append(
        "Redis Port 6379 Not Listening"
    )

if report["ssh_port"] == "NOT_FOUND":
    issues.append(
        "SSH Port 22 Not Listening"
    )

status = "READY FOR APPROVAL"

if issues:
    status = "REJECTED"

report["status"] = status
report["issues"] = issues

with open(
    "reports/server_report.json",
    "w"
) as file:

    json.dump(
        report,
        file,
        indent=4
    )

ssh.close()

if os.path.exists("temp_key.pem"):
    os.remove("temp_key.pem")

print("ServerCommon precheck completed")