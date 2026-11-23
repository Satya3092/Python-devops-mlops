"""
Day 006 — Type Conversion
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Basic conversions
# ======================================================================
port_text = "8080"
port_number = int(port_text)
print(port_number + 1)

price = float("19.99")
print(price * 2)

print(int(7.9))          # decimal part is cut off
print(round(7.9))        # round() rounds to nearest
print(str(443) + "/tcp")

print(bool(0), bool(1), bool(""), bool("False"))
print(3 + 2.5, type(3 + 2.5))   # implicit conversion to float

# ======================================================================
# Example 2 — Disk usage calculator from user input
# ======================================================================
total_gb = float(input("Total disk size (GB): "))
used_gb = float(input("Used space (GB): "))

free_gb = total_gb - used_gb
used_percent = used_gb / total_gb * 100

print("Free space:", free_gb, "GB")
print("Used:", round(used_percent, 1), "%")
print("Used (whole number):", int(used_percent), "%")
