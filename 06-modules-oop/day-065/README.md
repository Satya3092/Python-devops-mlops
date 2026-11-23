# Day 065 — Inheritance, Encapsulation, and Polymorphism

[⬅ Day 064](../../06-modules-oop/day-064/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 066 ➡](../../07-devops-automation/day-066/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 6 — Advanced Python and OOP | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Create child classes that inherit and extend a parent class (`super()`)
- Protect internal state with encapsulation (`_protected`, `__private`, `@property`)
- Use polymorphism and abstract base classes to treat different objects the same way

## 2. Topic Explanation

**1. Inheritance — reuse and extend.** A child class gets everything from its parent and can add or override behaviour.

```python
class Notifier:                      # parent (base class)
    def send(self, message): ...

class SlackNotifier(Notifier):       # child (subclass)
    def send(self, message): ...     # override
```
`super().__init__(...)` calls the parent's constructor so you don't repeat it.

Analogy: a Docker image `FROM python:3.12` — you inherit everything from the base image and add your own layers.

**2. Encapsulation — protect the internals.** Keep an object's data consistent by controlling access:
- `_name` — "internal, please don't touch" (convention).
- `__name` — name-mangled, harder to access from outside.
- `@property` — expose a value that looks like an attribute but runs code (validation, read-only values).

Analogy: a car's dashboard. You use the steering wheel and pedals (public interface); you don't adjust fuel injection directly.

**3. Polymorphism — same interface, different behaviour.** Different classes implement the same method name, so code can treat them uniformly: `for n in notifiers: n.send(msg)` works for Slack, email and SMS.

**Abstraction** with `abc.ABC` + `@abstractmethod` forces every subclass to implement required methods.

## 3. Syntax

```python
from abc import ABC, abstractmethod

class Base(ABC):
    def __init__(self, name):
        self._name = name                 # protected by convention

    @property
    def name(self):                       # read-only attribute
        return self._name

    @abstractmethod
    def run(self): ...

class Child(Base):
    def __init__(self, name, extra):
        super().__init__(name)            # reuse parent constructor
        self.extra = extra

    def run(self):                        # override
        return f"{self.name} running"
```

| Part | Meaning |
|---|---|
| `class Child(Base)` | Child inherits from Base. |
| `super().__init__()` | Calls the parent implementation. |
| `_attr / __attr` | Protected by convention / name-mangled private. |
| `@property` | Method accessed like an attribute; add a setter for validation. |
| `ABC + @abstractmethod` | Defines an interface subclasses must implement. |

## 4. Example 1 — Basic Example: Inheritance and method overriding

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"

    def introduce(self):
        return f"I am {self.name}. {self.speak()}"


class Dog(Animal):
    def speak(self):                       # override
        return f"{self.name} says woof"


class Cat(Animal):
    def __init__(self, name, indoor=True):
        super().__init__(name)             # reuse parent constructor
        self.indoor = indoor

    def speak(self):
        return f"{self.name} says meow"


animals = [Animal("Generic"), Dog("Rex"), Cat("Tom", indoor=False)]
for animal in animals:                     # polymorphism: same call, different behaviour
    print(animal.introduce())

print("Is a Dog an Animal?", isinstance(animals[1], Animal))
print("Cat indoor?", animals[2].indoor)
```

## 5. Example 2 — Practical Example: A pluggable alerting system

```python
from abc import ABC, abstractmethod


class Notifier(ABC):
    """Interface: every notifier must implement send()."""

    def __init__(self, name, min_severity=1):
        self._name = name
        self.__sent_count = 0              # private: changed only via notify()
        self.min_severity = min_severity

    @property
    def sent_count(self):                  # read-only from outside
        return self.__sent_count

    @property
    def min_severity(self):
        return self._min_severity

    @min_severity.setter
    def min_severity(self, value):         # validation on assignment
        if value not in (1, 2, 3):
            raise ValueError("severity must be 1, 2 or 3")
        self._min_severity = value

    def notify(self, message, severity):
        if severity < self.min_severity:
            return None
        self.__sent_count += 1
        return self.send(message, severity)

    @abstractmethod
    def send(self, message, severity):
        ...


class SlackNotifier(Notifier):
    def __init__(self, channel, **kwargs):
        super().__init__("slack", **kwargs)
        self.channel = channel

    def send(self, message, severity):
        return f"[Slack #{self.channel}] {'!' * severity} {message}"


class EmailNotifier(Notifier):
    def __init__(self, address, **kwargs):
        super().__init__("email", **kwargs)
        self.address = address

    def send(self, message, severity):
        return f"[Email to {self.address}] Subject: SEV{severity} alert - {message}"


class PagerNotifier(Notifier):
    def send(self, message, severity):
        return f"[PAGER] Waking up on-call: {message}"


notifiers = [
    SlackNotifier("alerts"),
    EmailNotifier("ops@example.com", min_severity=2),
    PagerNotifier("pager", min_severity=3),
]
events = [("Disk 80% on web-01", 1), ("API error rate 7%", 2), ("Database down", 3)]

for message, severity in events:
    for notifier in notifiers:              # polymorphism
        result = notifier.notify(message, severity)
        if result:
            print(result)

print("Sent counts:", {type(n).__name__: n.sent_count for n in notifiers})

try:
    notifiers[0].min_severity = 7
except ValueError as error:
    print("Validation:", error)
try:
    Notifier("abstract")
except TypeError as error:
    print("Cannot instantiate abstract class:", "abstract" in str(error))
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `Dog` and `Cat` inherit `introduce()` from `Animal` and override `speak()`.
- `Cat.__init__` calls `super().__init__(name)` and adds an extra attribute.
- The loop calls `introduce()` on each object; Python picks the right `speak()` for each class — **polymorphism**.

**Example 2**
- `Notifier(ABC)` defines the interface; `send` is abstract, so `Notifier(...)` itself cannot be created.
- **Encapsulation:** `__sent_count` can only change through `notify()`; `sent_count` is a read-only property; `min_severity` has a setter that validates values.
- **Inheritance:** subclasses reuse `notify()` (filtering + counting) and only implement `send()`.
- **Polymorphism:** the event loop doesn't care which notifier it is — adding Teams or SMS later means writing one new class, no changes to the loop.

## 7. Expected Output

**Example 1:**

```text
I am Generic. Generic makes a sound
I am Rex. Rex says woof
I am Tom. Tom says meow
Is a Dog an Animal? True
Cat indoor? False
```

**Example 2:**

```text
[Slack #alerts] ! Disk 80% on web-01
[Slack #alerts] !! API error rate 7%
[Email to ops@example.com] Subject: SEV2 alert - API error rate 7%
[Slack #alerts] !!! Database down
[Email to ops@example.com] Subject: SEV3 alert - Database down
[PAGER] Waking up on-call: Database down
Sent counts: {'SlackNotifier': 3, 'EmailNotifier': 2, 'PagerNotifier': 1}
Validation: severity must be 1, 2 or 3
Cannot instantiate abstract class: True
```

## 8. Common Mistakes

**1. Forgetting `super().__init__()`**

The child's `__init__` replaces the parent's; without calling `super()`, parent attributes are never set → `AttributeError`.

**2. Deep inheritance trees**

More than 2–3 levels gets confusing. Prefer composition (objects containing other objects) when 'is-a' doesn't fit.

**3. Treating `_private` as security**

Underscores are conventions, not protection. Never rely on them to hide secrets.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Shapes:** Create a base `Shape` with `area()` returning 0 and `describe()`. Create `Circle(r)` and `Square(side)` overriding `area()`. Print the description of a list of shapes and the total area.
- **Task 2 (Medium) — Encapsulated thermostat:** Create `Thermostat` with a `temperature` property whose setter only accepts 10–30 °C (raise ValueError otherwise) and a read-only `history` property returning a copy of all accepted values.
- **Task 3 (Practical Challenge) — Deployment strategies:** Create an abstract `DeploymentStrategy` with `deploy(version, hosts)`. Implement `RollingDeployment(batch_size)`, `BlueGreenDeployment()` and `CanaryDeployment(percent)` that return a list of step strings. Run all three polymorphically for 6 hosts and print the steps.

## 10. DevOps/MLOps Connection

- **DevOps:** pluggable notifiers, deployment strategies, cloud providers behind one interface (e.g. `StorageBackend` with S3/GCS/local implementations).
- **Cloud:** Terraform providers and Ansible connection plugins follow the same "common interface, many implementations" idea.
- **ML/MLOps:** every scikit-learn estimator implements `fit`/`predict` — that's polymorphism; you can swap `LinearRegression` for `RandomForestRegressor` without changing the pipeline code (Days 94–96).

## 11. Interview Questions

**Q1. What is polymorphism?**

<details><summary>Show answer</summary>

The ability of different classes to be used through the same interface; calling the same method name runs class-specific behaviour.

</details>

**Q2. What does `super()` do?**

<details><summary>Show answer</summary>

Returns a proxy to the parent class so you can call its methods, commonly `super().__init__(...)`.

</details>

**Q3. What is the purpose of an abstract base class?**

<details><summary>Show answer</summary>

To define a required interface; subclasses must implement abstract methods, and the ABC itself cannot be instantiated.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 65 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 064](../../06-modules-oop/day-064/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 066 ➡](../../07-devops-automation/day-066/README.md)
