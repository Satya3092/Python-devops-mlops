"""
Day 085 — NumPy Arrays and Operations
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Indexing, masks and aggregations
# ======================================================================
import numpy as np

cpu = np.array([45, 92, 71, 98, 33, 87])
print("first, last:", cpu[0], cpu[-1], "| slice 1:4:", cpu[1:4])
print("mask cpu > 85:", cpu > 85)
print("values > 85:", cpu[cpu > 85])
print("between 40 and 90:", cpu[(cpu >= 40) & (cpu <= 90)])
print("count > 85:", (cpu > 85).sum(), "| any > 95?", (cpu > 95).any(), "| all > 30?", (cpu > 30).all())
print("labels:", np.where(cpu > 85, "ALERT", "ok"))
print("sum/mean/std:", cpu.sum(), round(cpu.mean(), 2), round(cpu.std(), 2))
print("index of max:", cpu.argmax())
print("reshape to 2x3:\n", cpu.reshape(2, 3))

# ======================================================================
# Example 2 — A metrics matrix: servers × hours
# ======================================================================
import numpy as np

servers = np.array(["web-01", "web-02", "db-01", "cache-01"])
hours = np.array(["09:00", "10:00", "11:00", "12:00", "13:00"])
# rows = servers, columns = hours (CPU %)
cpu = np.array([
    [35, 42, 55, 61, 48],
    [70, 88, 93, 97, 85],
    [50, 52, 58, 60, 57],
    [20, 22, 19, 25, 21],
])
print("shape:", cpu.shape)
print("db-01 at 11:00:", cpu[2, 2])
print("all servers at 12:00:", dict(zip(servers, cpu[:, 3])))

print("average per server:", dict(zip(servers, cpu.mean(axis=1).round(1))))
print("peak per hour     :", dict(zip(hours, cpu.max(axis=0))))
busiest_hour = hours[cpu.sum(axis=0).argmax()]
print("busiest hour across the fleet:", busiest_hour)

hot = cpu > 90
print("readings over 90%:", hot.sum(), "on", servers[hot.any(axis=1)])

# Broadcasting: how far is each reading from that server's own average?
deviation = cpu - cpu.mean(axis=1, keepdims=True)
print("deviation from own average (web-02):", deviation[1].round(1))

# Min-max scaling to 0..1 per server (a common ML preprocessing step)
mins = cpu.min(axis=1, keepdims=True)
maxs = cpu.max(axis=1, keepdims=True)
print("scaled cache-01:", ((cpu - mins) / (maxs - mins))[3].round(2))
