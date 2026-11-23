"""
Day 020 — String Formatting (f-strings)
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — f-string basics
# ======================================================================
name = "Asha"
day = 20
progress = day / 100

print(f"Hello {name}, today is day {day}.")
print(f"Progress: {progress:.0%}")
print(f"Pi to 3 decimals: {3.14159265:.3f}")
print(f"Big number: {1234567890:,}")
print(f"Ticket number: {42:05d}")
print(f"Next day: {day + 1}")
print(f"{name=}, {day=}")

# ======================================================================
# Example 2 — A formatted server report table
# ======================================================================
servers = [
    ("web-01", 23.5, 41.0, 1_048_576),
    ("web-02", 87.25, 92.3, 524_288),
    ("db-01", 55.0, 78.75, 8_388_608),
]

print(f"{'HOST':<8} {'CPU%':>7} {'MEM%':>7} {'DISK(KB)':>12} {'STATUS':^10}")
print("-" * 48)
for host, cpu, mem, disk_kb in servers:              # loops: Day 29
    status = "ALERT" if cpu > 80 or mem > 90 else "ok"
    print(f"{host:<8} {cpu:>7.1f} {mem:>7.1f} {disk_kb:>12,} {status:^10}")

total_disk_gb = sum(s[3] for s in servers) / 1024 / 1024
print("-" * 48)
print(f"Total disk: {total_disk_gb:.2f} GB")
