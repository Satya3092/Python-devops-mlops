"""
Day 026 — Dictionaries
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Dictionary basics
# ======================================================================
student = {"name": "Asha", "course": "Python", "day": 26}
print(student)
print("Name:", student["name"])

student["day"] = 27                 # update existing key
student["city"] = "Pune"            # add new key
print("Updated:", student)

del student["course"]
print("After delete:", student)

print("Has 'city'?", "city" in student)
print("Email:", student.get("email", "not provided"))
print("Number of keys:", len(student))

# ======================================================================
# Example 2 — A Kubernetes deployment as a dictionary
# ======================================================================
deployment = {
    "name": "orders-api",
    "namespace": "prod",
    "replicas": 3,
    "image": "registry.example.com/orders-api:2.4.1",
    "labels": {"app": "orders", "tier": "backend"},
}

print(f"Deployment {deployment['name']} in namespace {deployment['namespace']}")
print("Replicas:", deployment["replicas"])
print("App label:", deployment["labels"]["app"])

# Scale up
deployment["replicas"] += 2
print("Scaled to:", deployment["replicas"])

# Read optional settings safely
cpu_limit = deployment.get("cpu_limit", "500m")
print("CPU limit (default if missing):", cpu_limit)

# Image tag is the text after the last ':'
tag = deployment["image"].split(":")[-1]
print("Image tag:", tag)
