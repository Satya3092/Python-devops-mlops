"""
Day 094 — Introduction to Scikit-Learn
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — The fit / predict / score pattern on the Iris dataset
# ======================================================================
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

iris = load_iris(as_frame=True)                   # bundled with scikit-learn, no download
X, y = iris.data, iris.target
print("Features:", list(X.columns))
print("Classes :", list(iris.target_names), "| samples:", len(X))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

for model in [KNeighborsClassifier(n_neighbors=5), LogisticRegression(max_iter=500), DecisionTreeClassifier(random_state=42)]:
    model.fit(X_train, y_train)                    # same API for every algorithm
    print(f"{type(model).__name__:<24} test accuracy = {model.score(X_test, y_test):.3f}")

flower = X_test.iloc[[0]]
best = LogisticRegression(max_iter=500).fit(X_train, y_train)
print("Prediction for first test flower:", iris.target_names[best.predict(flower)[0]],
      "| probabilities:", best.predict_proba(flower).round(3)[0].tolist())

# ======================================================================
# Example 2 — Preprocessing + model in one Pipeline, with cross-validation
# ======================================================================
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.read_csv("../../datasets/server_failures.csv")
# add a categorical feature so we can practise encoding
df["environment"] = ["prod" if i % 3 == 0 else "staging" if i % 3 == 1 else "dev" for i in range(len(df))]
numeric = ["cpu_usage", "memory_usage", "disk_usage", "error_count", "response_time_ms"]
categorical = ["environment"]
X, y = df[numeric + categorical], df["failure"]

preprocess = ColumnTransformer([
    ("num", StandardScaler(), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
])

for name, model in [("logistic_regression", LogisticRegression(max_iter=1000)),
                    ("random_forest", RandomForestClassifier(n_estimators=200, random_state=42))]:
    pipe = Pipeline([("preprocess", preprocess), ("model", model)])
    scores = cross_val_score(pipe, X, y, cv=5)
    print(f"{name:<20} 5-fold accuracy: {scores.mean():.3f} (+/- {scores.std():.3f})")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
pipe = Pipeline([("preprocess", preprocess), ("model", LogisticRegression(max_iter=1000))]).fit(X_train, y_train)
print("Pipeline steps:", list(pipe.named_steps))
print("Encoded feature names:", list(pipe.named_steps["preprocess"].get_feature_names_out())[-3:])
new_server = pd.DataFrame([{"cpu_usage": 93, "memory_usage": 91, "disk_usage": 88, "error_count": 7,
                            "response_time_ms": 650, "environment": "prod"}])
print("Failure probability for a stressed prod server:", round(pipe.predict_proba(new_server)[0, 1], 3))
