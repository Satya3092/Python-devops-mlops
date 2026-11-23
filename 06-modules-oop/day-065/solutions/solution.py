"""
Day 065 — Inheritance, Encapsulation, and Polymorphism: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import math
from abc import ABC, abstractmethod

# ===== Task 1 =====
class Shape:
    def area(self):
        return 0

    def describe(self):
        return f"{type(self).__name__} with area {self.area():.2f}"


class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self):
        return math.pi * self.r ** 2


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2


shapes = [Circle(1), Square(3)]
for s in shapes:
    print(s.describe())
print(f"Total area: {sum(s.area() for s in shapes):.2f}")

# ===== Task 2 =====
class Thermostat:
    def __init__(self):
        self._temperature = 20
        self._history = [20]

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if not 10 <= value <= 30:
            raise ValueError(f"{value} C is outside 10-30 C")
        self._temperature = value
        self._history.append(value)

    @property
    def history(self):
        return list(self._history)


t = Thermostat()
t.temperature = 23
try:
    t.temperature = 45
except ValueError as error:
    print("Rejected:", error)
t.temperature = 18
print("Current:", t.temperature, "History:", t.history)

# ===== Task 3 =====
class DeploymentStrategy(ABC):
    @abstractmethod
    def deploy(self, version, hosts):
        ...


class RollingDeployment(DeploymentStrategy):
    def __init__(self, batch_size):
        self.batch_size = batch_size

    def deploy(self, version, hosts):
        return [f"deploy {version} to {hosts[i:i + self.batch_size]}"
                for i in range(0, len(hosts), self.batch_size)]


class BlueGreenDeployment(DeploymentStrategy):
    def deploy(self, version, hosts):
        return [f"start green env with {version} on {len(hosts)} new hosts",
                "run smoke tests on green", "switch load balancer blue -> green",
                "keep blue for rollback"]


class CanaryDeployment(DeploymentStrategy):
    def __init__(self, percent):
        self.percent = percent

    def deploy(self, version, hosts):
        count = max(1, len(hosts) * self.percent // 100)
        return [f"deploy {version} to canary {hosts[:count]}", "watch error rate for 15 min",
                f"deploy {version} to remaining {len(hosts) - count} hosts"]


hosts = [f"web-0{i}" for i in range(1, 7)]
for strategy in [RollingDeployment(2), BlueGreenDeployment(), CanaryDeployment(20)]:
    print(f"== {type(strategy).__name__} ==")
    for step in strategy.deploy("v2.0", hosts):
        print("  ", step)
