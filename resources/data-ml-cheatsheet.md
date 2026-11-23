# pandas & scikit-learn Cheat Sheet

[⬅ Resources](README.md)

```python
import pandas as pd, numpy as np
df = pd.read_csv("data.csv", parse_dates=["timestamp"])
df.head(); df.info(); df.describe(); df.isna().sum(); df["env"].value_counts()
df[(df.cpu > 80) & (df.env == "prod")]; df.sort_values("cpu", ascending=False)
df.groupby("env").agg(avg_cpu=("cpu", "mean"), n=("host", "count"))
df.pivot_table(index="region", columns="product", values="revenue", aggfunc="sum")
df["col"] = df["col"].fillna(df["col"].median()); df.drop_duplicates()

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import classification_report, roc_auc_score, mean_absolute_error, r2_score
import joblib

X, y = df[features], df["label"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X_tr, y_tr)
print(classification_report(y_te, model.predict(X_te)))
print(roc_auc_score(y_te, model.predict_proba(X_te)[:, 1]))
cross_val_score(model, X, y, cv=5).mean()
joblib.dump(model, "model.joblib"); model = joblib.load("model.joblib")
```
