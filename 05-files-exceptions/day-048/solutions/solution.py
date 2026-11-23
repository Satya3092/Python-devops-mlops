"""
Day 048 — Writing Files: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
with open("table9.txt", "w", encoding="utf-8") as f:
    for n in range(1, 11):
        print(f"9 x {n} = {9 * n}", file=f)
with open("table9.txt", encoding="utf-8") as f:
    print(f.read(), end="")

# ===== Task 2 =====
for attempt in (1, 2):
    try:
        with open("release_notes.txt", "x", encoding="utf-8") as f:
            f.write("v1.0.0 - first release\n")
        print("Created release_notes.txt")
    except FileExistsError:
        print("release_notes.txt already exists")

# ===== Task 3 =====
backends = [("10.0.1.10", 8080), ("10.0.1.11", 8080), ("10.0.1.12", 8081)]
with open("upstream.conf", "w", encoding="utf-8") as f:
    f.write("upstream app_backend {\n")
    for ip, port in backends:
        f.write(f"    server {ip}:{port};\n")
    f.write("    keepalive 32;\n")
    f.write("}\n")
with open("upstream.conf", encoding="utf-8") as f:
    print(f.read(), end="")
