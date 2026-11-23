"""
Day 017 — String Indexing: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
region = "ap-south-1"
print(region[0])
print(region[-1])
print(region[3])

# ===== Task 2 =====
first = "Linus"
last = "Torvalds"
print(first[0] + "." + last[0] + ".")

# ===== Task 3 =====
perm = "drwxr-xr--"
print("Directory:", perm[0] == "d")
for name, start in [("owner", 1), ("group", 4), ("others", 7)]:
    print(name, "read:", perm[start] == "r", "write:", perm[start + 1] == "w", "execute:", perm[start + 2] == "x")
