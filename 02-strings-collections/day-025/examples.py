"""
Day 025 — Sets and Set Operations
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Set basics and operations
# ======================================================================
visitors = ["10.0.0.1", "10.0.0.2", "10.0.0.1", "10.0.0.3", "10.0.0.2"]
unique_visitors = set(visitors)
print("Unique IPs:", sorted(unique_visitors))
print("Count:", len(unique_visitors))

a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print("Union:", a | b)
print("Intersection:", a & b)
print("a - b:", a - b)
print("Symmetric diff:", a ^ b)

a.add(10)
a.discard(99)          # no error even though 99 is missing
print("After add/discard:", sorted(a))

# ======================================================================
# Example 2 — Configuration drift and access audit
# ======================================================================
# Packages that SHOULD be installed (desired state) vs what IS installed
desired_packages = {"nginx", "git", "curl", "python3", "fail2ban"}
installed_packages = {"nginx", "git", "curl", "python3", "telnet", "ftp"}

missing = desired_packages - installed_packages
unexpected = installed_packages - desired_packages
compliant = desired_packages & installed_packages

print("Missing (install these):", sorted(missing))
print("Unexpected (remove these):", sorted(unexpected))
print("Compliant:", sorted(compliant))
print("Fully compliant?", desired_packages <= installed_packages)

# Who has access to production but is no longer on the team?
team_members = {"asha", "ravi", "john"}
prod_access = {"asha", "ravi", "john", "old_contractor", "intern2024"}
print("Revoke access for:", sorted(prod_access - team_members))
