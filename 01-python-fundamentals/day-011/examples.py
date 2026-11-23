"""
Day 011 — Operator Precedence
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Seeing precedence in action
# ======================================================================
print("2 + 3 * 4     =", 2 + 3 * 4)
print("(2 + 3) * 4   =", (2 + 3) * 4)
print("2 ** 3 ** 2   =", 2 ** 3 ** 2)
print("(2 ** 3) ** 2 =", (2 ** 3) ** 2)
print("-3 ** 2       =", -3 ** 2)
print("(-3) ** 2     =", (-3) ** 2)
print("10 - 4 - 3    =", 10 - 4 - 3)
print("100 / 10 * 2  =", 100 / 10 * 2)

# ======================================================================
# Example 2 — Correct average and alert logic
# ======================================================================
web_01_cpu = 70
web_02_cpu = 90

wrong_average = web_01_cpu + web_02_cpu / 2      # bug!
right_average = (web_01_cpu + web_02_cpu) / 2
print("Wrong average:", wrong_average)
print("Right average:", right_average)

is_prod = False
cpu_high = True
disk_high = True
# Without parentheses: (is_prod and cpu_high) or disk_high
alert_unclear = is_prod and cpu_high or disk_high
# Intended: only alert for production
alert_correct = is_prod and (cpu_high or disk_high)
print("Alert (no parentheses):", alert_unclear)
print("Alert (with parentheses):", alert_correct)
