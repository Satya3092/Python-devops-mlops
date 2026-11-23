"""
Day 093 — Features, Labels, Training Data, and Testing Data: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

houses = pd.read_csv("../../datasets/house_prices.csv")
X = houses.drop(columns=["price"])
y = houses["price"]

# ===== Task 1 =====
print(list(X.columns), X.shape)
print(y.head(3).tolist())

# ===== Task 2 =====
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=7)
print(len(X_train), len(X_test))
print("mean price train/test:", round(y_train.mean()), round(y_test.mean()))
print("overlap:", len(set(X_train.index) & set(X_test.index)))

# ===== Task 3 =====
df = pd.read_csv("../../datasets/server_failures.csv")
df["incident_ticket_opened"] = df["failure"]
honest = ["cpu_usage", "memory_usage", "disk_usage", "error_count", "response_time_ms"]
for name, cols in [("honest", honest), ("leaky", honest + ["incident_ticket_opened"])]:
    X_train, X_test, y_train, y_test = train_test_split(df[cols], df["failure"], test_size=0.25,
                                                        random_state=42, stratify=df["failure"])
    acc = DecisionTreeClassifier(max_depth=3, random_state=42).fit(X_train, y_train).score(X_test, y_test)
    print(f"{name:<7} test accuracy: {acc:.3f}")
print("WARNING: 'incident_ticket_opened' only exists AFTER a failure, so it is unavailable at prediction time. "
      "The leaky model's perfect score would collapse in production.")
