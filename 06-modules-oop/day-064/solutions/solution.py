"""
Day 064 — Classes, Objects, and Constructors: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import json
from dataclasses import dataclass, field

# ===== Task 1 =====
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def __str__(self):
        return f"Rectangle {self.width}x{self.height}: area={self.area()} perimeter={self.perimeter()}"


print(Rectangle(3, 4))
print(Rectangle(10, 2))

# ===== Task 2 =====
class Service:
    registry = []

    def __init__(self, name, port, replicas=1):
        self.name = name
        self.port = port
        self.replicas = replicas
        Service.registry.append(name)

    def scale(self, n):
        if n < 0:
            raise ValueError("replicas cannot be negative")
        self.replicas = n

    def url(self):
        return f"http://{self.name}:{self.port}"

    def __repr__(self):
        return f"Service({self.name}, port={self.port}, replicas={self.replicas})"


api = Service("api", 8080)
worker = Service("worker", 9000, replicas=2)
api.scale(4)
print(api.url(), worker.url())
print(api, worker)
print("Registry:", Service.registry)

# ===== Task 3 =====
@dataclass
class Host:
    name: str
    ip: str
    env: str
    tags: list = field(default_factory=list)

    @classmethod
    def from_json(cls, text):
        return [cls(**item) for item in json.loads(text)]


data = '[{"name": "web-01", "ip": "10.0.0.5", "env": "prod", "tags": ["web"]},' \
       ' {"name": "db-01", "ip": "10.0.0.9", "env": "prod", "tags": ["db"]},' \
       ' {"name": "web-dev", "ip": "10.1.0.5", "env": "dev", "tags": ["web", "test"]}]'
hosts = Host.from_json(data)
by_env = {}
for h in hosts:
    by_env.setdefault(h.env, []).append(h.name)
print(by_env)
print("Web hosts:", [h.name for h in hosts if "web" in h.tags])
