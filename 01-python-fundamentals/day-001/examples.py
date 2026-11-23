"""
Day 001 — Introduction to Python, Installation, IDE, First Program
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Hello, World!
# ======================================================================
# My first Python program
print("Hello, World!")
print("I am learning Python for DevOps and MLOps.")
print("Day", 1, "of", 100)

# ======================================================================
# Example 2 — A deployment banner
# ======================================================================
# A banner like the ones CI/CD pipelines print in their logs
print("=" * 40)                  # "=" repeated 40 times
print("  Deploying: payment-service")
print("  Environment: staging")
print("  Version: 1.0.0")
print("=" * 40)
print("Step 1/3: Pulling Docker image")
print("Step 2/3: Running health checks")
print("Step 3/3: Switching traffic")
print("Deployment finished successfully!")
