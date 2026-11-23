"""
Day 014 — elif and Nested Conditions
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Grading with elif
# ======================================================================
score = 82

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print("Score", score, "-> grade", grade)

# ======================================================================
# Example 2 — Incident severity classifier
# ======================================================================
environment = "prod"
http_status = 503
error_rate = 12.5

if http_status >= 500:
    if environment == "prod":
        if error_rate > 10:
            severity = "SEV-1 (page on-call now)"
        else:
            severity = "SEV-2 (investigate within 1 hour)"
    elif environment in ("staging", "qa"):
        severity = "SEV-3 (fix during work hours)"
    else:
        severity = "SEV-4 (dev environment, low priority)"
elif http_status >= 400:
    severity = "Client error - check request logs"
else:
    severity = "OK"

print("Environment:", environment, "| Status:", http_status, "| Errors:", error_rate, "%")
print("Severity:", severity)
