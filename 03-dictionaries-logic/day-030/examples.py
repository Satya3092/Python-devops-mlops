"""
Day 030 — While Loops
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Counting with while
# ======================================================================
count = 5
while count > 0:
    print("Countdown:", count)
    count -= 1
print("Lift off!")

# Sum numbers until the total passes 20
total = 0
number = 1
while total <= 20:
    total += number
    number += 1
print("Total:", total, "after adding up to", number - 1)

# ======================================================================
# Example 2 — Retry with exponential backoff and polling
# ======================================================================
# Simulated health-check results: the service becomes healthy on the 4th try
health_results = [False, False, False, True]

MAX_ATTEMPTS = 5
attempt = 0
delay = 1
healthy = False

while attempt < MAX_ATTEMPTS and not healthy:
    healthy = health_results[attempt]
    attempt += 1
    if healthy:
        print(f"Attempt {attempt}: service is healthy")
    else:
        print(f"Attempt {attempt}: not ready, retrying in {delay}s")
        # time.sleep(delay)   # real code would wait here
        delay *= 2

if not healthy:
    print("Giving up after", MAX_ATTEMPTS, "attempts")

# Polling a rollout: replicas become ready one by one
desired_replicas = 3
ready_replicas = 0
checks = 0
while ready_replicas < desired_replicas:
    checks += 1
    ready_replicas += 1                 # simulate one pod becoming ready
    print(f"Check {checks}: {ready_replicas}/{desired_replicas} replicas ready")
print("Rollout complete")
