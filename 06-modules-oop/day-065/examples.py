"""
Day 065 — Inheritance, Encapsulation, and Polymorphism
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Inheritance and method overriding
# ======================================================================
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

# ======================================================================
# Example 2 — A pluggable alerting system
# ======================================================================
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
