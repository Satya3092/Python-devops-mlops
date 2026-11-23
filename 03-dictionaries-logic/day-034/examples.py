"""
Day 034 — List Comprehension
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Comprehension basics
# ======================================================================
numbers = [3, -1, 8, 0, -5, 12]

squares = [n ** 2 for n in numbers]
positives = [n for n in numbers if n > 0]
labels = ["pos" if n > 0 else "non-pos" for n in numbers]
print("Squares:", squares)
print("Positives:", positives)
print("Labels:", labels)

words = ["Docker", "Kubernetes", "Git"]
lengths = {word: len(word) for word in words}
first_letters = {word[0].lower() for word in words + ["Grafana"]}
print("Lengths:", lengths)
print("First letters:", sorted(first_letters))

# ======================================================================
# Example 2 — Transforming infrastructure data
# ======================================================================
instances = [
    {"id": "i-01", "state": "running", "type": "t3.micro", "env": "prod"},
    {"id": "i-02", "state": "stopped", "type": "t3.large", "env": "dev"},
    {"id": "i-03", "state": "running", "type": "m5.large", "env": "prod"},
    {"id": "i-04", "state": "running", "type": "t3.micro", "env": "dev"},
]

running_ids = [i["id"] for i in instances if i["state"] == "running"]
prod_types = [i["type"] for i in instances if i["env"] == "prod"]
id_to_state = {i["id"]: i["state"] for i in instances}
unique_types = sorted({i["type"] for i in instances})

print("Running:", running_ids)
print("Prod instance types:", prod_types)
print("State map:", id_to_state)
print("Unique types:", unique_types)

# Clean a list of raw lines from a config file
raw_lines = ["  nginx ", "", "# comment", "redis", "  postgres"]
packages = [line.strip() for line in raw_lines if line.strip() and not line.strip().startswith("#")]
print("Packages to install:", packages)

# Build docker commands
commands = [f"docker pull {image}:latest" for image in packages]
print(commands)
