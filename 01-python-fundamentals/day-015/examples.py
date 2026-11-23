"""
Day 015 — Python Fundamentals Revision and Mini Project
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Revision: all basics in one place
# ======================================================================
APP_NAME = "inventory-service"      # constant (str)
replicas = 3                        # int
cpu_limit = 0.5                     # float
is_public = False                   # bool

total_cpu = replicas * cpu_limit
print("App:", APP_NAME)
print("Total CPU requested:", total_cpu, "cores")
print("Type of total_cpu:", type(total_cpu).__name__)

if is_public:
    print("Exposed through a LoadBalancer")
else:
    print("Internal service (ClusterIP)")

# ======================================================================
# Example 2 — Mini project — Server Resource Alert Calculator
# ======================================================================
WARNING_LEVEL = 75
CRITICAL_LEVEL = 90

server_name = input("Server name: ")
cpu_percent = float(input("CPU usage %: "))
memory_total_gb = float(input("Total memory (GB): "))
memory_used_gb = float(input("Used memory (GB): "))
disk_total_gb = float(input("Total disk (GB): "))
disk_used_gb = float(input("Used disk (GB): "))

memory_percent = memory_used_gb / memory_total_gb * 100
disk_percent = disk_used_gb / disk_total_gb * 100

# Classify each resource
if cpu_percent >= CRITICAL_LEVEL:
    cpu_status = "CRITICAL"
elif cpu_percent >= WARNING_LEVEL:
    cpu_status = "WARNING"
else:
    cpu_status = "OK"

if memory_percent >= CRITICAL_LEVEL:
    memory_status = "CRITICAL"
elif memory_percent >= WARNING_LEVEL:
    memory_status = "WARNING"
else:
    memory_status = "OK"

if disk_percent >= CRITICAL_LEVEL:
    disk_status = "CRITICAL"
elif disk_percent >= WARNING_LEVEL:
    disk_status = "WARNING"
else:
    disk_status = "OK"

# Overall status = the worst individual status
if "CRITICAL" in (cpu_status, memory_status, disk_status):
    overall = "CRITICAL"
    action = "Page the on-call engineer now."
elif "WARNING" in (cpu_status, memory_status, disk_status):
    overall = "WARNING"
    action = "Create a ticket and watch the trend."
else:
    overall = "OK"
    action = "No action needed."

print()
print("=" * 40)
print("Resource report for", server_name)
print("=" * 40)
print("CPU    :", round(cpu_percent, 1), "% ->", cpu_status)
print("Memory :", round(memory_percent, 1), "% ->", memory_status)
print("Disk   :", round(disk_percent, 1), "% ->", disk_status)
print("-" * 40)
print("Overall:", overall)
print("Action :", action)
