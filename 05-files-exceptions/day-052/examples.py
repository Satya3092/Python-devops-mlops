"""
Day 052 — Exception Handling
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Catching common errors
# ======================================================================
values = ["42", "3.5", "abc", "100"]
for value in values:
    try:
        number = int(value)
        print(f"{value!r} -> {number}")
    except ValueError as error:
        print(f"{value!r} -> ValueError: {error}")

config = {"host": "localhost"}
try:
    print(config["port"])
except KeyError as error:
    print("Missing key:", error)

try:
    print(10 / 0)
except ZeroDivisionError:
    print("Cannot divide by zero")

try:
    with open("does_not_exist.txt", encoding="utf-8") as f:
        f.read()
except FileNotFoundError as error:
    print("File problem:", error.filename, "-", error.strerror)

# ======================================================================
# Example 2 — Robust parsing of messy metrics
# ======================================================================
raw_metrics = [
    "web-01,cpu,45.2",
    "web-02,cpu,ninety",          # bad number
    "web-03,cpu",                 # missing field
    "db-01,cpu,77.0",
    "",                           # empty line
    "db-02,cpu,0",
]

parsed = []
problems = []
for line_number, line in enumerate(raw_metrics, start=1):
    try:
        host, metric, value = line.split(",")
        parsed.append((host, metric, float(value)))
    except ValueError as error:
        problems.append(f"line {line_number}: {error}")

print("Parsed:", parsed)
print("Problems:")
for p in problems:
    print("  ", p)

# Use the clean data safely
values = [v for _, _, v in parsed]
try:
    ratio = values[0] / values[-1]
except ZeroDivisionError:
    ratio = None
except IndexError:
    ratio = None
print("Ratio first/last:", ratio)
