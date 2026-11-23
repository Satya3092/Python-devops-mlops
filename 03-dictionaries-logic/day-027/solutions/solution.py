"""
Day 027 — Dictionary Methods: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
capitals = {"India": "New Delhi", "Japan": "Tokyo", "France": "Paris"}
for country, capital in capitals.items():
    print(f"{country}: {capital}")
print(sorted(capitals.values()))

# ===== Task 2 =====
words = "deploy test deploy build test deploy".split()
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
for word, count in sorted(counts.items(), key=lambda pair: pair[1], reverse=True):
    print(word, count)

# ===== Task 3 =====
codes = [200, 200, 404, 500, 200, 301, 404, 200, 503, 200]
code_counts = {}
for code in codes:
    code_counts[code] = code_counts.get(code, 0) + 1
class_counts = {}
for code, count in code_counts.items():
    status_class = f"{code // 100}xx"
    class_counts[status_class] = class_counts.get(status_class, 0) + count
print("By code:", code_counts)
print("By class:", dict(sorted(class_counts.items())))
errors = class_counts.get("4xx", 0) + class_counts.get("5xx", 0)
print(f"Error percentage: {errors / len(codes) * 100:.1f}%")
