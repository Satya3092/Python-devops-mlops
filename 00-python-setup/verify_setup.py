"""verify_setup.py - check your Python environment for the 100-day course.

Run:  python 00-python-setup/verify_setup.py
"""
import importlib
import platform
import shutil
import sys

PHASE_PACKAGES = [
    ("Phase 7", ["psutil"]),
    ("Phase 8", ["requests", "yaml", "boto3"]),
    ("Phase 9", ["numpy", "pandas", "matplotlib", "openpyxl"]),
    ("Phase 10", ["sklearn", "joblib"]),
    ("Phase 11", ["fastapi", "uvicorn", "pydantic", "httpx"]),
]


def main():
    ok = sys.version_info >= (3, 10)
    print(f"Python {platform.python_version()} ({sys.executable})  ->  {'OK' if ok else 'please install Python 3.10+'}")
    in_venv = sys.prefix != sys.base_prefix
    print(f"Virtual environment active: {'yes' if in_venv else 'no (recommended: python -m venv .venv)'}")
    print("Days 1-65 need only the standard library: OK")
    for phase, modules in PHASE_PACKAGES:
        status = []
        for name in modules:
            try:
                module = importlib.import_module(name)
                status.append(f"{name} {getattr(module, '__version__', '')}".strip())
            except ImportError:
                status.append(f"{name} MISSING")
        missing = any("MISSING" in s for s in status)
        print(f"{phase:<9} {'needs install' if missing else 'ready':<14} " + ", ".join(status))
    for tool in ("git", "docker", "aws", "kubectl"):
        print(f"{tool:<8} {'found' if shutil.which(tool) else 'not found (needed only for later phases)'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
