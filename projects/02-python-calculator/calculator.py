"""
Project 2 - Python Calculator.

Run:   python calculator.py
Test:  pytest -q
"""
import math
import operator


class CalculatorError(Exception):
    """Raised for any user-facing calculation problem."""


def divide(a, b):
    if b == 0:
        raise CalculatorError("division by zero")
    return a / b


def floor_divide(a, b):
    if b == 0:
        raise CalculatorError("division by zero")
    return a // b


def modulo(a, b):
    if b == 0:
        raise CalculatorError("modulo by zero")
    return a % b


def power(a, b):
    if abs(b) > 1000:
        raise CalculatorError("exponent too large")
    return a ** b


def square_root(a):
    if a < 0:
        raise CalculatorError("square root of a negative number")
    return math.sqrt(a)


BINARY = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": divide,
          "//": floor_divide, "%": modulo, "**": power}
UNARY = {"sqrt": square_root, "abs": abs}


def to_number(text, last_result=None):
    """Convert text to int/float; 'ans' means the previous result."""
    if text == "ans":
        if last_result is None:
            raise CalculatorError("no previous result for 'ans'")
        return last_result
    try:
        value = float(text)
    except ValueError:
        raise CalculatorError(f"'{text}' is not a number") from None
    return int(value) if value.is_integer() else value


def tidy(value):
    """Show 84 instead of 84.0 and round long decimals."""
    if isinstance(value, float):
        value = round(value, 10)
        return int(value) if value.is_integer() else value
    return value


def calculate(line, last_result=None):
    """Evaluate one input line and return the result (raises CalculatorError)."""
    parts = line.split()
    if len(parts) == 4 and parts[0] == "percent" and parts[2] == "of":
        return tidy(to_number(parts[1], last_result) / 100 * to_number(parts[3], last_result))
    if len(parts) == 2 and parts[0] in UNARY:
        return tidy(UNARY[parts[0]](to_number(parts[1], last_result)))
    if len(parts) == 3:
        left, op, right = parts
        if op not in BINARY:
            raise CalculatorError(f"unknown operator '{op}' (use {' '.join(BINARY)})")
        return tidy(BINARY[op](to_number(left, last_result), to_number(right, last_result)))
    raise CalculatorError("use 'a op b', 'sqrt x', 'abs x' or 'percent x of y'")


HELP = """Examples:  12 + 3   7 / 2   2 ** 10   17 % 5   sqrt 16   abs -3   percent 20 of 150
Commands:  ans (last result), history, help, quit"""


def main():
    history = []
    last = None
    print("Python Calculator - type 'help' for commands, 'quit' to exit")
    while True:
        try:
            line = input("calc> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line in ("quit", "exit", "q"):
            break
        if line == "help":
            print(HELP)
            continue
        if line == "history":
            for number, entry in enumerate(history, start=1):
                print(f"{number}. {entry}")
            if not history:
                print("(empty)")
            continue
        try:
            last = calculate(line, last)
        except CalculatorError as error:
            print("Error:", error)
            continue
        history.append(f"{line} = {last}")
        print("=", last)
    print("Goodbye!")


if __name__ == "__main__":
    main()
