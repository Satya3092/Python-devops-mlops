"""
Day 005 — Input and Output
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Asking for a name
# ======================================================================
name = input("What is your name? ")
print("Hello,", name)
print("Welcome to Day 5!")

# ======================================================================
# Example 2 — Collecting deployment details
# ======================================================================
# Interactive prompt, like a small deployment wizard
app_name = input("Application name: ")
version = input("Version to deploy: ")
environment = input("Target environment: ")

print()                                              # empty line
print("Deployment summary")
print("App", "Version", "Env", sep=" | ")
print(app_name, version, environment, sep=" | ")
print("Image tag: ", app_name, ":", version, sep="")  # no spaces
print("Deploying", end="")                           # stay on same line
print("...", end="")
print(" done")
print("input() returns:", type(version))
