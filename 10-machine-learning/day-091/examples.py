"""
Day 091 — AI vs ML vs Deep Learning
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Rules written by a human vs rules learned from data
# ======================================================================
from sklearn.tree import DecisionTreeClassifier, export_text

# Each example: [cpu_percent, error_count]  -> label: 1 = incident followed, 0 = fine
examples = [[20, 0], [35, 1], [50, 0], [60, 2], [85, 1], [92, 0], [70, 6], [88, 7], [95, 5], [40, 8]]
labels = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]


def human_rule(cpu, errors):
    """What an engineer might write first."""
    return int(cpu > 90)


human_correct = sum(human_rule(c, e) == y for (c, e), y in zip(examples, labels))
print(f"Human rule correct on {human_correct}/{len(labels)} examples")

model = DecisionTreeClassifier(max_depth=2, random_state=42)
model.fit(examples, labels)                       # the machine learns the rules
print(f"Learned model correct on {(model.predict(examples) == labels).sum()}/{len(labels)} examples")
print("Rules the model learned:")
print(export_text(model, feature_names=["cpu", "errors"]))
print("Prediction for cpu=60, errors=9:", model.predict([[60, 9]])[0])

# ======================================================================
# Example 2 — A tiny neural network (the idea behind deep learning)
# ======================================================================
import numpy as np
from sklearn.neural_network import MLPClassifier

rng = np.random.default_rng(42)
# A pattern that is NOT a straight line: "risky" when cpu and memory are BOTH high or BOTH low
X = rng.uniform(0, 100, size=(400, 2))
y = ((X[:, 0] > 50) == (X[:, 1] > 50)).astype(int)

net = MLPClassifier(hidden_layer_sizes=(16, 16), max_iter=2000, random_state=42)
net.fit(X / 100, y)                               # scale inputs to 0..1
print("Layers (input -> hidden -> hidden -> output):", [2, 16, 16, 1])
print("Learned weights:", sum(w.size for w in net.coefs_), "| biases:", sum(b.size for b in net.intercepts_))
print("Training accuracy:", round(net.score(X / 100, y), 3))
for point in ([90, 95], [10, 5], [90, 10]):
    print(f"cpu={point[0]:>3} mem={point[1]:>3} -> predicted risky={net.predict(np.array([point]) / 100)[0]}")
