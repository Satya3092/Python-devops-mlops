"""
Day 057 — Python Packages
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Importing from a local package
# ======================================================================
import infra_tools
from infra_tools.naming import hostname
from infra_tools import is_valid_ip

print("Package version:", infra_tools.__version__)
print(hostname("orders", "prod", 1))
print(hostname("search", "dev", 12))

for ip in ["10.0.0.1", "256.1.1.1", "192.168.1", "172.16.5.20"]:
    print(f"{ip:<14} valid={is_valid_ip(ip)}")

# ======================================================================
# Example 2 — Inspecting the environment and installed packages
# ======================================================================
import sys
from importlib import metadata

in_venv = sys.prefix != sys.base_prefix
print("Running inside a virtual environment?", in_venv)
print("Python executable ends with:", sys.executable.split("/")[-1])

for package in ["requests", "PyYAML", "psutil", "not-a-real-package"]:
    try:
        version = metadata.version(package)
        print(f"{package:<20} installed, version {version}")
    except metadata.PackageNotFoundError:
        print(f"{package:<20} NOT installed -> pip install {package}")
