"""
Day 032 — Break, Continue, and Pass
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — break, continue, pass
# ======================================================================
for number in range(1, 10):
    if number == 6:
        print("Found 6, stopping")
        break
    if number % 2 == 0:
        continue                 # skip even numbers
    print("Odd number:", number)

for task in ["build", "test", "deploy"]:
    if task == "test":
        pass                     # TODO: add tests later
    print("Running", task)

# ======================================================================
# Example 2 — Scanning logs and searching for a free port
# ======================================================================
log_lines = [
    "INFO  Service starting",
    "",
    "# this is a comment",
    "INFO  Connected to database",
    "ERROR Out of memory",
    "INFO  This line is never read",
]

for line_number, line in enumerate(log_lines, start=1):
    if not line or line.startswith("#"):
        continue                                  # ignore blank lines and comments
    if line.startswith("ERROR"):
        print(f"First error at line {line_number}: {line}")
        break                                     # stop at the first error
    print(f"line {line_number} ok")

# Find the first free port (for ... else)
used_ports = {8000, 8001, 8002}
for port in range(8000, 8003):
    if port not in used_ports:
        print("Free port found:", port)
        break
else:
    print("No free port between 8000 and 8002")
