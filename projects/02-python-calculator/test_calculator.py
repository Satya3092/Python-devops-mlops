"""Unit tests for calculator.py - run with: pytest -q"""
import pytest

from calculator import CalculatorError, calculate


@pytest.mark.parametrize("line, expected", [
    ("12 + 3", 15), ("10 - 4", 6), ("6 * 7", 42), ("7 / 2", 3.5), ("17 // 5", 3),
    ("17 % 5", 2), ("2 ** 10", 1024), ("sqrt 16", 4), ("abs -3", 3), ("percent 20 of 150", 30),
])
def test_valid_expressions(line, expected):
    assert calculate(line) == expected


def test_ans_uses_last_result():
    assert calculate("ans * 2", last_result=21) == 42


@pytest.mark.parametrize("line", ["5 / 0", "5 // 0", "5 % 0", "sqrt -1", "ten + 1", "1 ^ 2", "1 +", "ans + 1"])
def test_errors_are_friendly(line):
    with pytest.raises(CalculatorError):
        calculate(line)
