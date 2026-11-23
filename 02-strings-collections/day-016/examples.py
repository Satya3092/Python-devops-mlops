"""
Day 016 — Strings Introduction
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — String basics
# ======================================================================
first_name = "Ada"
last_name = 'Lovelace'
full_name = first_name + " " + last_name

print(full_name)
print("Length:", len(full_name))
print("Contains 'love'?", "love" in full_name)
print("Contains 'Love'?", "Love" in full_name)
print("=" * 20)

quote = "It's a \"great\" day"
print(quote)

# ======================================================================
# Example 2 — Inspecting a log line
# ======================================================================
log_line = "2026-11-20 10:15:32 ERROR [payment-api] Database connection timeout"

print("Line length:", len(log_line), "characters")

if "ERROR" in log_line:
    print("This is an error line")

if "timeout" in log_line:
    print("Root cause hint: something timed out")

if "WARNING" not in log_line:
    print("Not a warning")

service = "payment-api"
alert = "ALERT: " + service + " reported an error"
print(alert)
