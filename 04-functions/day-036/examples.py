"""
Day 036 — Introduction to Functions
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Defining and calling a function
# ======================================================================
def print_banner():
    """Print a decorative banner."""
    print("=" * 30)
    print("   100 Days of Python")
    print("=" * 30)


print("Before calling")
print_banner()
print_banner()
print("Docstring:", print_banner.__doc__)

# ======================================================================
# Example 2 — Refactoring a script into functions
# ======================================================================
import platform
import datetime


def show_header():
    """Print the report header with the current date."""
    today = datetime.date(2026, 11, 20)        # fixed date so the output is stable
    print(f"Server report - {today}")
    print("-" * 32)


def show_system_info():
    """Print basic information about the machine running the script."""
    print("Python version  :", platform.python_version()[:4])
    print("Operating system:", platform.system())


def show_footer():
    """Print the closing line."""
    print("-" * 32)
    print("End of report")


def main():
    """Run the whole report: every step is one function call."""
    show_header()
    show_system_info()
    show_footer()


main()
