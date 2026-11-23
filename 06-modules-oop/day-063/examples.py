"""
Day 063 — Object-Oriented Programming Introduction
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Everything is an object
# ======================================================================
text = "web-01"
numbers = [3, 1, 2]
config = {"env": "prod"}

print(type(text), "->", text.upper())          # method of str
numbers.sort()                                  # method of list
print(type(numbers), "->", numbers)
print(type(config), "->", list(config.keys()))  # method of dict
print("Is a str an object?", isinstance(text, object))
print("Some methods of str:", [m for m in dir(text) if not m.startswith("_")][:8])

# ======================================================================
# Example 2 — From loose dicts and functions to a class
# ======================================================================
# Without OOP: data and functions are separate
server_a = {"name": "web-01", "cpu": 45}
server_b = {"name": "web-02", "cpu": 93}


def is_overloaded(server):
    return server["cpu"] > 90


print("Dict version:", is_overloaded(server_a), is_overloaded(server_b))


# With OOP: data + behaviour live together
class Server:
    def describe(self):
        status = "OVERLOADED" if self.is_overloaded() else "ok"
        return f"{self.name} cpu={self.cpu}% -> {status}"

    def is_overloaded(self):
        return self.cpu > 90


web_01 = Server()            # an object built from the blueprint
web_01.name = "web-01"       # (tomorrow you'll set these in a constructor)
web_01.cpu = 45

web_02 = Server()
web_02.name = "web-02"
web_02.cpu = 93

for server in (web_01, web_02):
    print(server.describe())
print("Same class, different objects:", type(web_01) is type(web_02), web_01 is web_02)
