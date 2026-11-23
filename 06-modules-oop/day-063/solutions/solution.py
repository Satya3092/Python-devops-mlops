"""
Day 063 — Object-Oriented Programming Introduction: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
for value in [42, 3.14, "hi", [1], (1,), {"a": 1}]:
    methods = [m for m in dir(value) if not m.startswith("_")]
    print(f"{type(value).__name__:<6} {len(methods)} public methods")

# ===== Task 2 =====
class Dog:
    def bark(self):
        return f"{self.name} says woof"


rex = Dog()
rex.name = "Rex"
bella = Dog()
bella.name = "Bella"
print(rex.bark())
print(bella.bark())

# ===== Task 3 =====
class Container:
    def start(self):
        self.state = "running"

    def stop(self):
        self.state = "exited"

    def status(self):
        return f"{self.name}: {getattr(self, 'state', 'created')}"


web = Container()
web.name = "web"
worker = Container()
worker.name = "worker"
print(web.status(), "|", worker.status())
web.start()
worker.start()
worker.stop()
print(web.status(), "|", worker.status())
