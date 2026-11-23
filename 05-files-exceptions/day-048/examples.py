"""
Day 048 — Writing Files
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Three ways to write
# ======================================================================
with open("notes.txt", "w", encoding="utf-8") as f:
    chars = f.write("First line written with write()\n")
    f.writelines(["Second line\n", "Third line\n"])
    print("Fourth line via print, value =", 42, file=f)

print("write() returned:", chars, "characters")

with open("notes.txt", encoding="utf-8") as f:
    print(f.read(), end="")

# "w" overwrites everything
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("Replaced!\n")
with open("notes.txt", encoding="utf-8") as f:
    print("After overwrite:", f.read().strip())

# ======================================================================
# Example 2 — Generating an Ansible inventory and a .env file
# ======================================================================
servers = [
    {"host": "web-01", "ip": "10.0.1.10", "group": "web"},
    {"host": "web-02", "ip": "10.0.1.11", "group": "web"},
    {"host": "db-01", "ip": "10.0.2.10", "group": "db"},
]

groups = {}
for s in servers:
    groups.setdefault(s["group"], []).append(s)

with open("inventory.ini", "w", encoding="utf-8") as inv:
    for group, members in groups.items():
        print(f"[{group}]", file=inv)
        for m in members:
            print(f"{m['host']} ansible_host={m['ip']}", file=inv)
        print(file=inv)                        # blank line between groups

settings = {"APP_ENV": "staging", "LOG_LEVEL": "INFO", "DB_HOST": "10.0.2.10", "DB_PORT": 5432}
with open(".env.example", "w", encoding="utf-8") as env_file:
    env_file.writelines(f"{key}={value}\n" for key, value in settings.items())

for name in ("inventory.ini", ".env.example"):
    print(f"----- {name} -----")
    with open(name, encoding="utf-8") as f:
        print(f.read().strip())
