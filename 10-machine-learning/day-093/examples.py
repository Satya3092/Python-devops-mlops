"""
Day 093 — Features, Labels, Training Data, and Testing Data
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Features, labels and a stratified split
# ======================================================================
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("../../datasets/server_failures.csv")
feature_columns = ["cpu_usage", "memory_usage", "disk_usage", "error_count", "response_time_ms"]
X = df[feature_columns]
y = df["failure"]
print("X shape:", X.shape, "| y shape:", y.shape)
print("Class balance (all):", y.value_counts(normalize=True).round(3).to_dict())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print("Train:", X_train.shape, "Test:", X_test.shape)
print("Failure rate train/test:", round(y_train.mean(), 3), "/", round(y_test.mean(), 3))
print("No overlap between sets:", set(X_train.index).isdisjoint(X_test.index))
print(X_train.head(3))

# ======================================================================
# Example 2 — Overfitting vs underfitting in action
# ======================================================================
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv("../../datasets/server_failures.csv")
X = df[["cpu_usage", "memory_usage", "disk_usage", "error_count", "response_time_ms"]]
y = df["failure"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

print(f"{'max_depth':>9} {'train acc':>10} {'test acc':>9}  verdict")
for depth in [1, 3, 5, None]:
    tree = DecisionTreeClassifier(max_depth=depth, random_state=42).fit(X_train, y_train)
    train_acc = tree.score(X_train, y_train)
    test_acc = tree.score(X_test, y_test)
    gap = train_acc - test_acc
    verdict = "overfitting (memorised)" if gap > 0.1 else "underfitting?" if train_acc < 0.85 else "good balance"
    print(f"{str(depth):>9} {train_acc:>10.3f} {test_acc:>9.3f}  {verdict}")

baseline = max(y_test.mean(), 1 - y_test.mean())
print(f"Baseline (always predict 'no failure'): {baseline:.3f}  <- any model must beat this")
