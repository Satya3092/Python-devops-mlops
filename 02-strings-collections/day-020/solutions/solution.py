"""
Day 020 — String Formatting (f-strings): reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
service = "orders"
replicas = 3
version = "2.1.0"
print(f"{service} v{version} running with {replicas} replicas")

# ===== Task 2 =====
request_count = 1532874
latency = 0.234567
success_ratio = 0.98765
print(f"Requests: {request_count:,}")
print(f"Latency: {latency * 1000:.1f} ms")
print(f"Success: {success_ratio:.2%}")

# ===== Task 3 =====
pods = [("api-7d9f", "Running", 0, 12.3), ("worker-5c2a", "CrashLoopBackOff", 14, 0.0), ("redis-0", "Running", 1, 3.75)]
print(f"{'NAME':<14}{'STATUS':<20}{'RESTARTS':>8}{'AGE':>8}")
for name, status, restarts, age in pods:
    print(f"{name:<14}{status:<20}{restarts:>8}{age:>7.1f}h")
