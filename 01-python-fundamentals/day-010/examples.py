"""
Day 010 — Assignment Operators
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Updating a counter
# ======================================================================
retries = 0
retries += 1
retries += 1
print("Retries:", retries)

backoff_seconds = 1
backoff_seconds *= 2
backoff_seconds *= 2
print("Next backoff:", backoff_seconds, "seconds")

message = "Build"
message += " passed"
print(message)

# ======================================================================
# Example 2 — Tracking request statistics
# ======================================================================
total_requests = 0
failed_requests = 0
total_latency_ms = 0

# Simulate three batches of traffic
total_requests += 1200
failed_requests += 6
total_latency_ms += 1200 * 85

total_requests += 800
failed_requests += 14
total_latency_ms += 800 * 140

total_requests += 1500
failed_requests += 3
total_latency_ms += 1500 * 90

average_latency = total_latency_ms / total_requests
error_rate = failed_requests / total_requests * 100

print("Total requests:", total_requests)
print("Failed requests:", failed_requests)
print("Average latency:", round(average_latency, 1), "ms")
print("Error rate:", round(error_rate, 2), "%")
