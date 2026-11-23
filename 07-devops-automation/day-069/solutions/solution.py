"""
Day 069 — System Information and Resource Monitoring: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import psutil

# ===== Task 1 =====
print(f"CPU: {psutil.cpu_percent(interval=1)}% | Memory: {psutil.virtual_memory().percent}% "
      f"| Disk: {psutil.disk_usage('/').percent}%")

# ===== Task 2 =====
cpu_samples = []
for i in range(1, 4):
    cpu = psutil.cpu_percent(interval=1)
    cpu_samples.append(cpu)
    print(f"Sample {i}: cpu={cpu}% mem={psutil.virtual_memory().percent}%")
print(f"Average CPU: {sum(cpu_samples) / len(cpu_samples):.1f}% | Peak CPU: {max(cpu_samples)}%")

# ===== Task 3 =====
heavy = []
count = 0
for proc in psutil.process_iter(["pid", "name", "memory_percent"]):
    count += 1
    try:
        if (proc.info["memory_percent"] or 0) > 1.0:
            heavy.append(proc.info)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue
heavy.sort(key=lambda p: p["memory_percent"], reverse=True)
print("Processes using > 1.0% memory:")
for p in heavy:
    print(f"  {p['name']} (pid {p['pid']}): {p['memory_percent']:.1f}%")
print(f"Total memory used by them: {sum(p['memory_percent'] for p in heavy):.1f}%")
print("Process count:", count)
