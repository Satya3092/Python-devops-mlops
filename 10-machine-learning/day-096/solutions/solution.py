"""
Day 096 — Classification and Model Evaluation: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import json

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

# ===== Task 1 =====
actual = [1, 0, 1, 1, 0, 0, 1, 0]
pred = [1, 0, 0, 1, 0, 1, 1, 0]
tp = sum(a == 1 and p == 1 for a, p in zip(actual, pred))
fp = sum(a == 0 and p == 1 for a, p in zip(actual, pred))
fn = sum(a == 1 and p == 0 for a, p in zip(actual, pred))
tn = sum(a == 0 and p == 0 for a, p in zip(actual, pred))
precision, recall = tp / (tp + fp), tp / (tp + fn)
f1 = 2 * precision * recall / (precision + recall)
print(f"TP={tp} FP={fp} FN={fn} TN={tn} precision={precision:.2f} recall={recall:.2f} f1={f1:.2f}")
print(f"sklearn: precision={precision_score(actual, pred):.2f} recall={recall_score(actual, pred):.2f} f1={f1_score(actual, pred):.2f}")

# ===== Task 2 =====
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.3, random_state=42, stratify=iris.target)
tree = DecisionTreeClassifier(max_depth=3, random_state=42).fit(X_train, y_train)
print(confusion_matrix(y_test, tree.predict(X_test)))
print(classification_report(y_test, tree.predict(X_test), target_names=iris.target_names, digits=3))

# ===== Task 3 =====
df = pd.read_csv("../../datasets/server_failures.csv")
X, y = df.drop(columns=["failure"]), df["failure"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]
chosen = None
for threshold in np.arange(0.05, 0.96, 0.05).round(2):
    pred = (proba >= threshold).astype(int)
    if recall_score(y_test, pred) >= 0.85:
        chosen = (float(threshold), precision_score(y_test, pred), recall_score(y_test, pred), int(pred.sum()))
threshold, precision, recall, alerts = chosen
print(f"threshold={threshold} precision={precision:.2f} recall={recall:.2f} alerts={alerts}")
with open("metrics.json", "w") as f:
    json.dump({"threshold": threshold, "precision": round(precision, 3), "recall": round(recall, 3)}, f)
print(open("metrics.json").read())
