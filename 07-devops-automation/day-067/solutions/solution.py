"""
Day 067 — Working with Environment Variables: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import os

# ===== Task 1 =====
def greet():
    print(f"Hello, {os.getenv('USER_NAME', 'stranger')}!")


os.environ.pop("USER_NAME", None)
greet()
os.environ["USER_NAME"] = "Asha"
greet()

# ===== Task 2 =====
def env_int(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        print(f"WARNING: {name}={value!r} is not an int, using {default}")
        return default


def env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


os.environ.update({"MAX_RETRIES": "5", "TIMEOUT": "abc", "VERBOSE": "yes"})
print(env_int("MAX_RETRIES", 3), env_int("TIMEOUT", 30), env_bool("VERBOSE"))

# ===== Task 3 =====
SENSITIVE = ("PASSWORD", "SECRET", "TOKEN")


def validate_env(required):
    return [name for name in required if not os.getenv(name)]


required = ["DB_HOST", "DB_USER", "DB_PASSWORD", "REDIS_URL"]
os.environ.update({"DB_HOST": "db.internal", "DB_USER": "app", "DB_PASSWORD": "hunter2"})
for name in required:
    value = os.getenv(name, "<missing>")
    if any(word in name for word in SENSITIVE) and value != "<missing>":
        value = "****"
    print(f"{name:<12} = {value}")
try:
    missing = validate_env(required)
    if missing:
        raise SystemExit(1)
except SystemExit as exit_signal:
    print(f"Missing variables: {missing} -> exit code {exit_signal.code}")
