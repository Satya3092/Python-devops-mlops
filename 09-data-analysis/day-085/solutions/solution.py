"""
Day 085 — NumPy Arrays and Operations: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import numpy as np

# ===== Task 1 =====
temps = np.array([22.5, 35.1, 28.4, 40.2, 18.9, 31.0])
print(temps[temps > 30], (temps > 30).sum())
print(np.where(temps > 35, 35, temps))

# ===== Task 2 =====
services = np.array(["api", "web", "worker"])
requests = np.array([[1200, 1350, 1500, 1800], [900, 950, 1100, 1000], [400, 420, 380, 500]])
print("per service:", dict(zip(services, requests.sum(axis=1).tolist())))
print("per quarter:", requests.sum(axis=0).tolist())
print("top service:", services[requests.sum(axis=1).argmax()])

# ===== Task 3 =====
rng = np.random.default_rng(3)
times = rng.normal(200, 20, size=50)
times[[10, 37]] = 450
z = (times - times.mean()) / times.std()
anomalies = np.where(np.abs(z) > 3)[0]
for i in anomalies:
    print(f"index {i}: {times[i]:.1f} ms (z={z[i]:.1f})")
