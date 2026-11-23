"""
Day 092 — Supervised vs Unsupervised Learning
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Same data, two kinds of question
# ======================================================================
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression

df = pd.read_csv("../../datasets/server_failures.csv")
X = df[["cpu_usage", "memory_usage", "disk_usage", "error_count"]]

# Supervised - CLASSIFICATION: label is a category (0/1)
classifier = LogisticRegression(max_iter=1000).fit(X, df["failure"])
print("Classification -> failure for a busy server?",
      classifier.predict(pd.DataFrame([[95, 92, 90, 8]], columns=X.columns))[0])

# Supervised - REGRESSION: label is a number
regressor = LinearRegression().fit(X, df["response_time_ms"])
print("Regression -> predicted response time:",
      round(regressor.predict(pd.DataFrame([[95, 92, 90, 8]], columns=X.columns))[0]), "ms")

print("Labels available? classification y:", df["failure"].unique().tolist(),
      "| regression y range:", (int(df["response_time_ms"].min()), int(df["response_time_ms"].max())))

# ======================================================================
# Example 2 — Unsupervised: clustering servers and spotting anomalies
# ======================================================================
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(42)
# Three hidden workload types (we DON'T tell the algorithm): web, database, batch
web = rng.normal([40, 30, 200], [5, 5, 30], size=(30, 3))       # cpu %, memory %, network Mbps
db = rng.normal([55, 85, 60], [5, 4, 15], size=(30, 3))
batch = rng.normal([90, 50, 20], [4, 6, 8], size=(30, 3))
odd = np.array([[5, 98, 900]])                                  # one strange server
X = np.vstack([web, db, batch, odd])

X_scaled = StandardScaler().fit_transform(X)                    # put features on the same scale
kmeans = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X_scaled)
for cluster in range(3):
    members = X[kmeans.labels_ == cluster]
    print(f"cluster {cluster}: {len(members):>2} servers, mean cpu={members[:, 0].mean():5.1f} "
          f"mem={members[:, 1].mean():5.1f} net={members[:, 2].mean():6.1f}")

iso = IsolationForest(contamination=0.01, random_state=42).fit(X_scaled)
flags = iso.predict(X_scaled)                                   # -1 = anomaly
print("anomalies found at rows:", np.where(flags == -1)[0].tolist())
print("row 90 values:", X[90].round(1).tolist())
