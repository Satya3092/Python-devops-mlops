"""
Day 045 — Functions Revision and Mini Project: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
def c_to_f(c):
    return c * 9 / 5 + 32


def f_to_c(f):
    return (f - 32) * 5 / 9


def c_to_k(c):
    return c + 273.15


CONVERSIONS = {"c->f": c_to_f, "f->c": f_to_c, "c->k": c_to_k}
for name, func in CONVERSIONS.items():
    print(f"100 {name}: {round(func(100), 2)}")

# ===== Task 2 =====
def stats(*values, precision=2):
    ordered = sorted(values)
    n = len(ordered)
    middle = n // 2
    median = ordered[middle] if n % 2 else (ordered[middle - 1] + ordered[middle]) / 2
    return {
        "count": n,
        "min": ordered[0],
        "max": ordered[-1],
        "mean": round(sum(ordered) / n, precision),
        "median": round(median, precision),
    }


print(stats(*[120, 87, 450, 134, 98, 101]))

# ===== Task 3 =====
def safe(func):
    def wrapper(a, b):
        if b == 0:
            return None
        return func(a, b)
    return wrapper


OPERATIONS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": safe(lambda a, b: a / b),
    "%": safe(lambda a, b: a % b),
    "//": safe(lambda a, b: a // b),
}


def calculate(expression, history):
    a, op, b = expression.split()
    if op not in OPERATIONS:
        return f"unknown operator {op}"
    result = OPERATIONS[op](float(a), float(b))
    if result is None:
        return "division by zero"
    history.append(f"{expression} = {result}")
    return result


history = []
for expr in ["17 % 5", "17 // 5", "8 // 0", "3 * 4"]:
    print(expr, "->", calculate(expr, history))
print("History:")
for entry in history:
    print(" ", entry)
