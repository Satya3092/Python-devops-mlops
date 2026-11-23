# Day 064 — Classes, Objects, and Constructors

[⬅ Day 063](../../06-modules-oop/day-063/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 065 ➡](../../06-modules-oop/day-065/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 6 — Advanced Python and OOP | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Initialise objects with the `__init__` constructor
- Use instance attributes, class attributes and methods
- Add `__str__`/`__repr__` and use `@dataclass` for simple data classes

## 2. Topic Explanation

The **constructor** `__init__` runs automatically when an object is created. It sets up the object's initial attributes:

```python
class Server:
    def __init__(self, name, ip, cpu_cores=2):
        self.name = name            # instance attribute
        self.ip = ip
        self.cpu_cores = cpu_cores

web = Server("web-01", "10.0.0.5")  # __init__ runs here
```

- **Instance attributes** (`self.name`) belong to one object.
- **Class attributes** (defined directly in the class body) are shared by all objects — good for constants and counters.
- **Methods** use `self` to read/update the object's attributes.
- **Special ("dunder") methods** customise behaviour: `__str__` (what `print()` shows), `__repr__` (developer view), `__len__`, `__eq__`...
- `@classmethod` gives alternative constructors, e.g. `Server.from_dict(data)`.

For classes that mainly **hold data**, `@dataclass` writes `__init__`, `__repr__` and `__eq__` for you:

```python
from dataclasses import dataclass

@dataclass
class Pod:
    name: str
    restarts: int = 0
```

## 3. Syntax

```python
class ClassName:
    class_attribute = "shared"

    def __init__(self, param1, param2=default):
        self.param1 = param1
        self.param2 = param2

    def method(self):
        return self.param1

    def __str__(self):
        return f"ClassName({self.param1})"
```

| Part | Meaning |
|---|---|
| `__init__` | Constructor — runs when an object is created. |
| `self.x = x` | Stores an instance attribute. |
| `class attribute` | Shared by all instances. |
| `__str__` | Human-friendly text for print(). |
| `@dataclass` | Auto-generates __init__/__repr__/__eq__ from type-annotated fields. |

## 4. Example 1 — Basic Example: A class with a constructor

```python
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
```

## 5. Example 2 — Practical Example: Modelling servers and pods

```python
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
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `__init__` stores `owner` and `balance` on each new object.
- `bank_name` is a class attribute — shared by every account.
- Methods change the object's own state (`self.balance`).
- `__str__` controls what `print(acc1)` shows.

**Example 2**
- `instances_created` counts objects across the class.
- `@classmethod from_dict` builds a `Server` from a dict — great for inventory files.
- `schedule()` is a tiny version of the Kubernetes scheduler: place the pod if enough CPU is free.
- `@dataclass Pod` gets `__init__`, `__repr__` and `__eq__` for free. `field(default_factory=dict)` avoids the mutable-default trap (Day 39).

## 7. Expected Output

**Example 1:**

```text
Asha's account at PyBank: 150
Ravi's account at PyBank: 20
Error: insufficient funds
```

**Example 2:**

```text
api-1     -> node-1
api-2     -> node-1
worker-1  -> node-2
db-0      -> node-2
Server('node-1', cpu 1.0/2) Server('node-2', cpu 3.5/4)
Servers created: 2
Pod(name='db-0', cpu=2, labels={'tier': 'db'})
Equal pods? True
```

## 8. Common Mistakes

**1. `def __init__(name):`**

Forgetting `self` causes `TypeError`. Every instance method's first parameter is `self`.

**2. Not storing parameters**

Writing `name = name` instead of `self.name = name` creates a local variable that disappears.

**3. Mutable class attributes**

`class Server: pods = []` shares ONE list across all servers. Create per-object lists in `__init__`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Rectangle:** Create `Rectangle(width, height)` with `area()`, `perimeter()` and `__str__`. Create two rectangles and print them.
- **Task 2 (Medium) — Service class:** Create `Service(name, port, replicas=1)` with `scale(n)` (validate n ≥ 0), `url()` returning `http://<name>:<port>` and `__repr__`. Keep a class attribute listing all created service names.
- **Task 3 (Practical Challenge) — Inventory from JSON:** Create a `@dataclass Host` with `name`, `ip`, `env` and `tags` (default empty list). Add a `classmethod` `from_json(text)` that returns a list of Host objects from a JSON array string. Load 3 hosts, then print hosts per environment and all hosts tagged `web`.

## 10. DevOps/MLOps Connection

- **DevOps:** model infrastructure (`Server`, `Deployment`, `Pipeline`) as classes in internal tools; load them from YAML/JSON with alternative constructors.
- **Cloud:** boto3 *resources* are objects (`s3.Bucket("logs").objects.all()`).
- **MLOps:** dataclasses/Pydantic models describe API requests, configs and experiment parameters (Day 98 uses Pydantic models, which look like dataclasses).

## 11. Interview Questions

**Q1. What does `__init__` do?**

<details><summary>Show answer</summary>

It initialises a newly created instance (it's the initializer/constructor) by setting its attributes.

</details>

**Q2. What is the difference between instance and class attributes?**

<details><summary>Show answer</summary>

Instance attributes belong to one object (`self.x`); class attributes are defined in the class body and shared by all instances.

</details>

**Q3. What does `@dataclass` generate?**

<details><summary>Show answer</summary>

`__init__`, `__repr__` and `__eq__` (and optionally ordering, frozen/immutability) from annotated fields.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 64 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 063](../../06-modules-oop/day-063/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 065 ➡](../../06-modules-oop/day-065/README.md)
