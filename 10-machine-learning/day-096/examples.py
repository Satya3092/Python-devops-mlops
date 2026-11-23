"""
Day 096 — Classification and Model Evaluation
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Metrics by hand: why accuracy can lie
# ======================================================================
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

actual = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]           # 2 real failures out of 10
lazy_model = [0] * 10                              # always "no failure"
alert_model = [0, 0, 0, 0, 0, 1, 1, 0, 1, 1]       # catches both, 2 false alarms

for name, predicted in [("lazy", lazy_model), ("alerting", alert_model)]:
    tn, fp, fn, tp = confusion_matrix(actual, predicted).ravel()
    print(f"{name:<9} TN={tn} FP={fp} FN={fn} TP={tp} | "
          f"accuracy={accuracy_score(actual, predicted):.2f} "
          f"precision={precision_score(actual, predicted, zero_division=0):.2f} "
          f"recall={recall_score(actual, predicted):.2f} "
          f"f1={f1_score(actual, predicted, zero_division=0):.2f}")
print("The lazy model is 80% accurate but catches 0 failures (recall 0.00)!")

# ======================================================================
# Example 2 — Predicting server failures and choosing a threshold
# ======================================================================
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("../../datasets/server_failures.csv")
X, y = df.drop(columns=["failure"]), df["failure"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

models = {
    "logistic_regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "random_forest": RandomForestClassifier(n_estimators=300, max_depth=6, random_state=42),
}
for name, model in models.items():
    model.fit(X_train, y_train)
    proba = model.predict_proba(X_test)[:, 1]
    print(f"{name:<20} ROC AUC = {roc_auc_score(y_test, proba):.3f}")

best = models["logistic_regression"]
proba = best.predict_proba(X_test)[:, 1]
print("\nDefault threshold 0.5:")
print(confusion_matrix(y_test, best.predict(X_test)))
print(classification_report(y_test, best.predict(X_test), target_names=["ok", "failure"], digits=3))

print("Threshold trade-off (missed failure = expensive):")
print(f"{'threshold':>9} {'precision':>9} {'recall':>7} {'alerts':>7} {'missed':>7}")
for threshold in (0.2, 0.3, 0.5, 0.7):
    pred = (proba >= threshold).astype(int)
    missed = int(((pred == 0) & (y_test == 1)).sum())
    print(f"{threshold:>9} {precision_score(y_test, pred, zero_division=0):>9.2f} "
          f"{recall_score(y_test, pred):>7.2f} {pred.sum():>7} {missed:>7}")

importances = pd.Series(models["random_forest"].feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nRandom forest feature importance:", importances.round(3).to_dict())
