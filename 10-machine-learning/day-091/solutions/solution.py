"""
Day 091 — AI vs ML vs Deep Learning: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
from sklearn.tree import DecisionTreeClassifier

# ===== Task 1 =====
scenarios = [
    ("Alert when disk > 90%", "AI-rule", "explicit threshold written by a human"),
    ("Predict next week's traffic", "ML", "learn trends from historical numbers"),
    ("Detect defects in photos", "DL", "images need deep neural networks"),
    ("Runbook chatbot", "DL", "generative large language model"),
    ("Cluster similar log messages", "ML", "unsupervised learning groups similar text"),
]
for task, kind, reason in scenarios:
    print(f"{task:<30} {kind:<8} {reason}")

# ===== Task 2 =====
examples = [[20, 0], [35, 1], [50, 0], [60, 2], [85, 1], [92, 0], [70, 6], [88, 7], [95, 5], [40, 8]]
labels = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]


def my_rule(cpu, errors):
    return int(cpu > 90 or errors >= 5)


print("My rule:", sum(my_rule(c, e) == y for (c, e), y in zip(examples, labels)), "/ 10")
tree = DecisionTreeClassifier(max_depth=2, random_state=42).fit(examples, labels)
print("Tree   :", int((tree.predict(examples) == labels).sum()), "/ 10")

# ===== Task 3 =====
problems = [
    {"name": "Disk full alerts", "has_labels": False, "data_volume": "low", "rules_known": True},
    {"name": "Predict deployment failures", "has_labels": True, "data_volume": "high", "rules_known": False},
    {"name": "Group noisy alerts", "has_labels": False, "data_volume": "high", "rules_known": False},
    {"name": "Forecast cloud cost", "has_labels": True, "data_volume": "low", "rules_known": False},
]


def recommend(p):
    if p["rules_known"]:
        return "simple rules"
    if p["data_volume"] == "low":
        return "collect data first"
    return "supervised ML" if p["has_labels"] else "unsupervised ML"


for p in problems:
    print(f"{p['name']:<28} -> {recommend(p)}")
