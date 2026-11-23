"""
Day 013 — if-else
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Even or odd
# ======================================================================
number = 7

if number % 2 == 0:
    print(number, "is even")
else:
    print(number, "is odd")

label = "even" if number % 2 == 0 else "odd"
print("Using a conditional expression:", label)

# ======================================================================
# Example 2 — Deployment gate
# ======================================================================
branch = input("Branch name: ")
tests_passed = input("Did tests pass? (yes/no): ").strip().lower() == "yes"

if branch == "main":
    target = "production"
else:
    target = "preview"

if tests_passed:
    print("Tests passed. Deploying to", target)
else:
    print("Tests failed. Deployment blocked!")

exit_code = 0 if tests_passed else 1
print("Pipeline exit code:", exit_code)
