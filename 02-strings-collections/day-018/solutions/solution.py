"""
Day 018 — String Slicing: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
filename = "backup-2026-11-20.tar.gz"
print(filename[-6:])
print(filename[7:17])

# ===== Task 2 =====
for word in ["level", "deploy"]:
    print(word, "is palindrome:", word == word[::-1])

# ===== Task 3 =====
api_key = "AKIAIOSFODNN7EXAMPLE"
masked = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
print(masked)
