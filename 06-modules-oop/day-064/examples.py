"""
Day 064 — Classes, Objects, and Constructors
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — A class with a constructor
# ======================================================================
class BankAccount:
    bank_name = "PyBank"                 # class attribute (shared)

    def __init__(self, owner, balance=0):
        self.owner = owner               # instance attributes
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
        return self.balance

    def __str__(self):
        return f"{self.owner}'s account at {self.bank_name}: {self.balance}"


acc1 = BankAccount("Asha", 100)
acc2 = BankAccount("Ravi")
acc1.deposit(50)
acc2.deposit(20)
print(acc1)
print(acc2)
try:
    acc2.withdraw(500)
except ValueError as error:
    print("Error:", error)

# ======================================================================
# Example 2 — Modelling servers and pods
# ======================================================================
from dataclasses import dataclass, field


class Server:
    instances_created = 0                       # class attribute counter

    def __init__(self, name, ip, cpu_cores=2, memory_gb=4):
        self.name = name
        self.ip = ip
        self.cpu_cores = cpu_cores
        self.memory_gb = memory_gb
        self.pods = []
        Server.instances_created += 1

    @classmethod
    def from_dict(cls, data):
        """Alternative constructor, e.g. from JSON/YAML inventory."""
        return cls(data["name"], data["ip"], data.get("cpu", 2), data.get("memory", 4))

    def schedule(self, pod):
        if self.cpu_used() + pod.cpu > self.cpu_cores:
            return False
        self.pods.append(pod)
        return True

    def cpu_used(self):
        return sum(p.cpu for p in self.pods)

    def __repr__(self):
        return f"Server({self.name!r}, cpu {self.cpu_used()}/{self.cpu_cores})"


@dataclass
class Pod:
    name: str
    cpu: float
    labels: dict = field(default_factory=dict)


node1 = Server("node-1", "10.0.0.11", cpu_cores=2)
node2 = Server.from_dict({"name": "node-2", "ip": "10.0.0.12", "cpu": 4})
pods = [Pod("api-1", 0.5), Pod("api-2", 0.5), Pod("worker-1", 1.5), Pod("db-0", 2, {"tier": "db"})]

for pod in pods:
    placed_on = next((n for n in (node1, node2) if n.schedule(pod)), None)
    print(f"{pod.name:<9} -> {placed_on.name if placed_on else 'PENDING (no capacity)'}")

print(node1, node2)
print("Servers created:", Server.instances_created)
print(pods[3])
print("Equal pods?", Pod("x", 1) == Pod("x", 1))
