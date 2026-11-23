"""
Day 021 — Lists
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Working with a list
# ======================================================================
tools = ["git", "docker", "kubernetes"]
print(tools)
print("Count:", len(tools))

tools.append("terraform")
print("After append:", tools)

tools[0] = "github"
print("After change:", tools)

tools.remove("docker")
print("After remove:", tools)

print("Is kubernetes in the list?", "kubernetes" in tools)
print("Sorted copy:", sorted(tools))
print("Original order kept:", tools)

# ======================================================================
# Example 2 — Response-time statistics
# ======================================================================
response_times_ms = [120, 98, 250, 134, 87, 1500, 143, 110]

print("Samples:", len(response_times_ms))
print("Fastest:", min(response_times_ms), "ms")
print("Slowest:", max(response_times_ms), "ms")
average = sum(response_times_ms) / len(response_times_ms)
print(f"Average: {average:.1f} ms")

sorted_times = sorted(response_times_ms)
middle = len(sorted_times) // 2
median = (sorted_times[middle - 1] + sorted_times[middle]) / 2
print(f"Median: {median:.1f} ms  (less affected by the 1500 ms outlier)")

slow_requests = []
for t in response_times_ms:           # loops are covered on Day 29
    if t > 200:
        slow_requests.append(t)
print("Slow requests (>200 ms):", slow_requests)
