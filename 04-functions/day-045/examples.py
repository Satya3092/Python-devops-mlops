"""
Day 045 — Functions Revision and Mini Project
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Functions are values
# ======================================================================
def shout(text):
    return text.upper() + "!"


def whisper(text):
    return text.lower() + "..."


styles = {"loud": shout, "quiet": whisper}
for name, func in styles.items():
    print(f"{name:<6}-> {func('Deploy complete')}")

pipeline = [str.strip, str.lower, lambda s: s.replace(" ", "-")]
value = "  Payment Service  "
for step in pipeline:
    value = step(value)
print("Slug:", value)

# ======================================================================
# Example 2 — Mini project — Calculator with a dispatch table
# ======================================================================
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return None                 # signal "cannot compute"
    return a / b


def power(a, b):
    return a ** b


OPERATIONS = {"+": add, "-": subtract, "*": multiply, "/": divide, "**": power}


def parse_number(text):
    """Return a float, or None if the text is not a number."""
    text = text.strip()
    if text.replace(".", "", 1).lstrip("-").isdigit():
        return float(text)
    return None


def calculate(expression):
    """Evaluate 'a op b' and return (ok, result_or_message)."""
    parts = expression.split()
    if len(parts) != 3:
        return False, "use the format: number operator number"
    a, op, b = parse_number(parts[0]), parts[1], parse_number(parts[2])
    if a is None or b is None:
        return False, "operands must be numbers"
    if op not in OPERATIONS:
        return False, f"unknown operator '{op}' (use {' '.join(OPERATIONS)})"
    result = OPERATIONS[op](a, b)
    if result is None:
        return False, "division by zero"
    return True, round(result, 4)


def main():
    expressions = ["12 + 30", "7 / 2", "2 ** 10", "5 / 0", "9 % 2", "ten * 3", "4 *"]
    for expression in expressions:
        ok, value = calculate(expression)
        label = "=" if ok else "error:"
        print(f"{expression:<10} {label} {value}")


main()
