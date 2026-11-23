"""
Day 094 — Introduction to Scikit-Learn: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

# ===== Task 1 =====
iris = load_iris(as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.25, random_state=1)
knn = KNeighborsClassifier(n_neighbors=3).fit(X_train, y_train)
print("accuracy:", round(knn.score(X_test, y_test), 3))
sample = pd.DataFrame([[5.9, 3.0, 5.1, 1.8]], columns=iris.data.columns)
print("prediction:", iris.target_names[knn.predict(sample)[0]])

# ===== Task 2 =====
scaler = StandardScaler().fit([[10], [20], [30]])
print("mean:", scaler.mean_, "scale:", scaler.scale_)
print(scaler.transform([[20], [40]]))
print((np.array([[20], [40]]) - scaler.mean_) / scaler.scale_)

# ===== Task 3 =====
df = pd.read_csv("../../datasets/server_failures.csv")
X, y = df.drop(columns=["failure"]), df["failure"]
results = []
for model in [LogisticRegression(max_iter=1000), DecisionTreeClassifier(max_depth=4, random_state=42),
              RandomForestClassifier(n_estimators=100, random_state=42)]:
    scores = cross_val_score(make_pipeline(StandardScaler(), model), X, y, cv=5)
    results.append((type(model).__name__, scores.mean()))
for rank, (name, score) in enumerate(sorted(results, key=lambda r: r[1], reverse=True), start=1):
    print(f"{rank}. {name:<24} {score:.3f}")
print("Winner:", max(results, key=lambda r: r[1])[0])
