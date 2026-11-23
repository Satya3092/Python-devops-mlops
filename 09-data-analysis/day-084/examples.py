"""
Day 084 — NumPy Introduction
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Creating and inspecting arrays
# ======================================================================
import numpy as np

cpu = np.array([45, 72, 91, 38])
print("array:", cpu, "| type:", type(cpu).__name__)
print("shape:", cpu.shape, "ndim:", cpu.ndim, "dtype:", cpu.dtype, "size:", cpu.size)

matrix = np.array([[45, 60, 70], [80, 85, 90]])
print("2-D shape:", matrix.shape)

print("zeros :", np.zeros(3))
print("ones  :", np.ones((2, 2), dtype=int).tolist())
print("full  :", np.full(3, 99))
print("arange:", np.arange(0, 60, 15))
print("linspace:", np.linspace(0, 1, 5))

rng = np.random.default_rng(42)
print("random ints:", rng.integers(0, 100, size=5))

print("list  * 2:", [1, 2, 3] * 2)
print("array * 2:", np.array([1, 2, 3]) * 2)

# ======================================================================
# Example 2 — Why NumPy: speed and vectorised maths on metrics
# ======================================================================
import time

import numpy as np

rng = np.random.default_rng(7)
latencies = rng.normal(loc=120, scale=25, size=1_000_000).clip(5)   # one million fake latencies (ms)
latency_list = latencies.tolist()

start = time.perf_counter()
slow_list = sum(1 for v in latency_list if v > 200)
list_seconds = time.perf_counter() - start

start = time.perf_counter()
slow_numpy = int((latencies > 200).sum())
numpy_seconds = time.perf_counter() - start

print("Slow requests (list) :", slow_list)
print("Slow requests (numpy):", slow_numpy)
print(f"NumPy was about {list_seconds / numpy_seconds:.0f}x faster")

seconds = latencies / 1000                       # vectorised unit conversion
print("first 3 in seconds:", np.round(seconds[:3], 4))
print(f"mean={latencies.mean():.1f} ms  p95={np.percentile(latencies, 95):.1f} ms  max={latencies.max():.1f} ms")
print("memory: list ~", len(latency_list) * 32 // 1024 // 1024, "MB vs array", latencies.nbytes // 1024 // 1024, "MB")
