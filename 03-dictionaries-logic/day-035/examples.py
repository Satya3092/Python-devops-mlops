"""
Day 035 — Programming Logic Practice and Mini Project
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Logic practice: FizzBuzz for deployments
# ======================================================================
# Classic FizzBuzz, DevOps flavour:
# build number divisible by 3 -> "lint", by 5 -> "scan", by both -> "full-pipeline"
for build in range(1, 16):
    if build % 15 == 0:
        print(build, "full-pipeline")
    elif build % 3 == 0:
        print(build, "lint")
    elif build % 5 == 0:
        print(build, "scan")
    else:
        print(build, "build-only")

# ======================================================================
# Example 2 — Mini project — Inventory Report Generator
# ======================================================================
inventory = [
    {"host": "web-01", "env": "prod", "os": "ubuntu-24.04", "cpu": 4, "ram_gb": 8, "cpu_util": 45, "owner": "team-web"},
    {"host": "web-02", "env": "prod", "os": "ubuntu-20.04", "cpu": 4, "ram_gb": 8, "cpu_util": 91, "owner": "team-web"},
    {"host": "db-01", "env": "prod", "os": "rhel-9", "cpu": 16, "ram_gb": 64, "cpu_util": 62, "owner": "team-data"},
    {"host": "web-01", "env": "staging", "os": "ubuntu-24.04", "cpu": 2, "ram_gb": 4, "cpu_util": 12, "owner": ""},
    {"host": "batch-01", "env": "dev", "os": "ubuntu-18.04", "cpu": 8, "ram_gb": 16, "cpu_util": 5, "owner": "team-ml"},
]
OUTDATED_OS = {"ubuntu-18.04", "ubuntu-20.04"}
HIGH_UTIL = 85

# 1. Group by environment
by_env = {}
for server in inventory:
    by_env.setdefault(server["env"], []).append(server)

# 2. Totals per environment
print("=== Capacity per environment ===")
for env, servers in by_env.items():
    total_cpu = sum(s["cpu"] for s in servers)
    total_ram = sum(s["ram_gb"] for s in servers)
    hosts = ", ".join(s["host"] for s in servers)
    print(f"{env:<8} servers={len(servers)} cpu={total_cpu:<3} ram={total_ram:<3}GB [{hosts}]")

# 3. Rule violations
print("\n=== Violations ===")
violations = []
for s in inventory:
    name = f"{s['env']}/{s['host']}"
    if not s["owner"]:
        violations.append((name, "missing owner tag"))
    if s["os"] in OUTDATED_OS:
        violations.append((name, f"outdated OS {s['os']}"))
    if s["cpu_util"] >= HIGH_UTIL:
        violations.append((name, f"high CPU {s['cpu_util']}%"))
for name, reason in violations:
    print(f"- {name:<16} {reason}")

# 4. Summary
affected = {name for name, _ in violations}
print("\n=== Summary ===")
print(f"Servers: {len(inventory)} | with issues: {len(affected)} | violations: {len(violations)}")
compliance = (len(inventory) - len(affected)) / len(inventory) * 100
print(f"Compliance: {compliance:.0f}%")
