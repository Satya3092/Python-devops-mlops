"""
Day 051 — Working with JSON
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Python ↔ JSON
# ======================================================================
import json

server = {"name": "web-01", "ports": [80, 443], "healthy": True, "owner": None, "cpu": 0.75}
text = json.dumps(server)
print("JSON string:", text)
print("Type:", type(text).__name__)

print("Pretty:")
print(json.dumps(server, indent=2, sort_keys=True))

api_response = '{"status": "ok", "count": 2, "items": [{"id": 1}, {"id": 2}], "next": null}'
data = json.loads(api_response)
print("Parsed type:", type(data).__name__)
print("Count:", data["count"], "| First id:", data["items"][0]["id"], "| Next:", data["next"])

# ======================================================================
# Example 2 — Reading, updating and saving a JSON config file
# ======================================================================
import json

config = {
    "service": "orders-api",
    "version": "2.4.1",
    "replicas": 3,
    "env": {"LOG_LEVEL": "INFO", "FEATURE_NEW_CHECKOUT": False},
    "healthcheck": {"path": "/health", "interval_seconds": 10},
}

with open("service_config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)
print("Saved config")

# Later (another script / another day): load, modify, save
with open("service_config.json", encoding="utf-8") as f:
    loaded = json.load(f)

loaded["version"] = "2.5.0"
loaded["replicas"] += 2
loaded["env"]["FEATURE_NEW_CHECKOUT"] = True
loaded["env"]["LOG_LEVEL"] = "DEBUG"

with open("service_config.json", "w", encoding="utf-8") as f:
    json.dump(loaded, f, indent=2)

with open("service_config.json", encoding="utf-8") as f:
    print(f.read())

# Sets are not JSON serialisable - convert them first
tags = {"prod", "web"}
try:
    json.dumps({"tags": tags})
except TypeError as error:
    print("TypeError:", error)
print(json.dumps({"tags": sorted(tags)}))
