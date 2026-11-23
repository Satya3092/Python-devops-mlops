"""
Day 035 — Programming Logic Practice and Mini Project: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
primes = []
for n in range(2, 51):
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            break
    else:
        primes.append(n)
print(primes)

# ===== Task 2 =====
values = [45, 91, 23, 91, 78, 60]
largest = second = None
for v in values:
    if largest is None or v > largest:
        largest, second = v, largest
    elif v != largest and (second is None or v > second):
        second = v
print(second)

# ===== Task 3 =====
inventory = [
    {"host": "web-01", "env": "prod", "cpu_util": 45, "owner": "team-web"},
    {"host": "web-02", "env": "prod", "cpu_util": 91, "owner": "team-web"},
    {"host": "db-01", "env": "prod", "cpu_util": 62, "owner": "team-data"},
    {"host": "web-01", "env": "staging", "cpu_util": 12, "owner": ""},
    {"host": "batch-01", "env": "dev", "cpu_util": 5, "owner": "team-ml"},
]
by_env = {}
for s in inventory:
    by_env.setdefault(s["env"], []).append(s)
for env, servers in by_env.items():
    busiest = max(servers, key=lambda s: s["cpu_util"])
    print(f"Busiest in {env}: {busiest['host']} ({busiest['cpu_util']}%)")
owners = {}
for s in inventory:
    owner = s["owner"] or "UNASSIGNED"
    owners[owner] = owners.get(owner, 0) + 1
print("Servers per owner:", owners)
for env, servers in by_env.items():
    average = sum(s["cpu_util"] for s in servers) / len(servers)
    if average > 50:
        print(f"Recommendation: scale up {env} (average CPU {average:.1f}%)")
