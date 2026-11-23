# Python Basics Cheat Sheet

[⬅ Resources](README.md)

```python
# Variables & types
name, port, ratio, active, nothing = "web-01", 8080, 0.75, True, None
type(port); isinstance(port, int); int("42"); str(42); float("3.5")

# Strings
s = "  Hello DevOps  "
s.strip().lower(); s.replace("Hello", "Hi"); s.split(); ",".join(["a", "b"])
s[0], s[-1], s[2:7], s[::-1]; f"{name}:{port}"; f"{ratio:.1%}"; "ops" in s

# Lists / tuples / sets / dicts
servers = ["web-01", "web-02"]; servers.append("db-01"); servers[1:]; len(servers)
point = (10, 20); x, y = point
tags = {"prod", "web"}; tags | {"linux"}; tags & {"prod"}; tags - {"web"}
cfg = {"env": "prod", "replicas": 3}; cfg.get("region", "us-east-1"); cfg.items()

# Conditions & loops
if cpu > 90: ...
elif cpu > 75: ...
else: ...
for i, host in enumerate(servers, start=1): ...
while retries < 3: retries += 1
[h.upper() for h in servers if h.startswith("web")]
{h: len(h) for h in servers}

# Functions
def deploy(service, version="latest", *hosts, dry_run=True, **labels):
    """Docstring."""
    return f"{service}:{version}"
sorted(items, key=lambda x: x["cpu"], reverse=True)

# Files & exceptions
with open("app.log", encoding="utf-8") as f:
    for line in f: ...
try:
    value = int(text)
except ValueError as error:
    print(error)
else: ...
finally: ...

# Classes
class Server:
    def __init__(self, name): self.name = name
    def __repr__(self): return f"Server({self.name!r})"
```
