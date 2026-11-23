"""
Day 069 — System Information and Resource Monitoring
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — A snapshot of the machine
# ======================================================================
import datetime
import psutil

GB = 1024 ** 3

cpu = psutil.cpu_percent(interval=1)
per_core = psutil.cpu_percent(interval=1, percpu=True)
mem = psutil.virtual_memory()
swap = psutil.swap_memory()
disk = psutil.disk_usage("/")
boot = datetime.datetime.fromtimestamp(psutil.boot_time())

print(f"CPU usage      : {cpu}% over {psutil.cpu_count()} logical cores")
print(f"Per core       : {per_core}")
print(f"Memory         : {mem.used / GB:.1f} / {mem.total / GB:.1f} GB ({mem.percent}%)")
print(f"Available mem  : {mem.available / GB:.1f} GB")
print(f"Swap used      : {swap.percent}%")
print(f"Disk /         : {disk.used / GB:.1f} / {disk.total / GB:.1f} GB ({disk.percent}%)")
print(f"Booted at      : {boot:%Y-%m-%d %H:%M}")
print(f"Uptime (hours) : {(datetime.datetime.now() - boot).total_seconds() / 3600:.1f}")

# ======================================================================
# Example 2 — Network throughput and the top processes
# ======================================================================
import time
import psutil

# Network rate = difference between two samples / elapsed time
before = psutil.net_io_counters()
time.sleep(2)
after = psutil.net_io_counters()
sent_rate = (after.bytes_sent - before.bytes_sent) / 2 / 1024
recv_rate = (after.bytes_recv - before.bytes_recv) / 2 / 1024
print(f"Network: sent {sent_rate:.1f} KB/s, received {recv_rate:.1f} KB/s")

# Top 5 processes by memory
processes = []
for proc in psutil.process_iter(["pid", "name", "username", "memory_percent"]):
    try:
        processes.append(proc.info)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue
top = sorted(processes, key=lambda p: p["memory_percent"] or 0, reverse=True)[:5]
print(f"{'PID':>7}  {'NAME':<18}{'USER':<12}{'MEM%':>6}")
for p in top:
    print(f"{p['pid']:>7}  {(p['name'] or '?')[:17]:<18}{(p['username'] or '?')[:11]:<12}{p['memory_percent'] or 0:>6.1f}")

# Mounted filesystems that are getting full
for part in psutil.disk_partitions(all=False):
    try:
        usage = psutil.disk_usage(part.mountpoint)
    except PermissionError:
        continue
    flag = "  <-- check!" if usage.percent > 80 else ""
    print(f"{part.mountpoint:<12} {part.fstype:<6} {usage.percent:>5.1f}%{flag}")
