"""
Day 025 — Sets and Set Operations: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
tags = ["web", "prod", "web", "api", "prod", "linux"]
unique_tags = set(tags)
print(sorted(unique_tags))
print(f"Removed {len(tags) - len(unique_tags)} duplicates")

# ===== Task 2 =====
my_skills = {"linux", "git", "docker", "kubernetes", "aws"}
mlops_skills = {"python", "docker", "kubernetes", "mlflow", "aws", "fastapi"}
print("Already have:", sorted(my_skills & mlops_skills))
print("Need to learn:", sorted(mlops_skills - my_skills))
print("All skills:", sorted(my_skills | mlops_skills))

# ===== Task 3 =====
allowed_ports = {22, 80, 443}
required_ports = {80, 443}
servers = [("web-01", {22, 80, 443, 8080}), ("web-02", {80, 443})]
for name, open_ports in servers:
    unauthorised = open_ports - allowed_ports
    missing = required_ports - open_ports
    verdict = "COMPLIANT" if not unauthorised and not missing else "NON-COMPLIANT"
    print(f"{name}: unauthorised={sorted(unauthorised)} missing={sorted(missing)} -> {verdict}")
print("Open on both:", sorted(servers[0][1] & servers[1][1]))
