"""
Day 033 — Nested Loops: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
for row in range(1, 6):
    numbers = []
    for n in range(1, row + 1):
        numbers.append(str(n))
    print(" ".join(numbers))

# ===== Task 2 =====
inventory = {"dev": ["web-01"], "staging": ["web-01", "web-02"], "prod": ["web-01", "web-02", "web-03", "db-01"]}
for env, hosts in inventory.items():
    for host in hosts:
        print(f"{env}/{host}")
for env, hosts in inventory.items():
    print(f"{env}: {len(hosts)} hosts")

# ===== Task 3 =====
hosts = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
ports = [22, 80, 443, 3306]
open_pairs = {("10.0.0.1", 22), ("10.0.0.1", 80), ("10.0.0.2", 443), ("10.0.0.3", 3306), ("10.0.0.3", 22)}
header = f"{'HOST':<10}" + "".join(f"{port:>7}" for port in ports)
print(header)
mysql_hosts = []
for host in hosts:
    row = f"{host:<10}"
    for port in ports:
        state = "OPEN" if (host, port) in open_pairs else "closed"
        row += f"{state:>7}"
        if port == 3306 and state == "OPEN":
            mysql_hosts.append(host)
    print(row)
print("MySQL exposed on:", mysql_hosts)
