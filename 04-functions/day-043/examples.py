"""
Day 043 — Scope and Local/Global Variables
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Local vs global
# ======================================================================
message = "I am global"


def show():
    local_message = "I am local"
    print(local_message)
    print(message)              # reading a global works


show()
try:
    print(local_message)
except NameError as error:
    print("NameError:", error)


def shadow():
    message = "I am a local with the same name"   # new local, global untouched
    print(message)


shadow()
print(message)

# ======================================================================
# Example 2 — Global counters vs returning values
# ======================================================================
# Version 1: global state (works, but harder to test)
errors_seen = 0


def scan_line_global(line):
    global errors_seen
    if "ERROR" in line:
        errors_seen += 1


for line in ["INFO ok", "ERROR db", "ERROR disk"]:
    scan_line_global(line)
print("Global counter:", errors_seen)


# Version 2: pure function - input in, result out (preferred)
def count_errors(lines):
    count = 0                       # local
    for line in lines:
        if "ERROR" in line:
            count += 1
    return count


print("Returned count:", count_errors(["INFO ok", "ERROR db", "ERROR disk"]))


# Enclosing scope with nonlocal: a counter factory
def make_counter():
    total = 0

    def increment(step=1):
        nonlocal total
        total += step
        return total

    return increment


request_counter = make_counter()
request_counter()
request_counter()
print("Requests counted:", request_counter(5))
