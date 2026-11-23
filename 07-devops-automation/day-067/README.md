# Day 067 — Working with Environment Variables

[⬅ Day 066](../../07-devops-automation/day-066/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 068 ➡](../../07-devops-automation/day-068/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 7 — Python for DevOps Automation | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Read environment variables safely with defaults and type conversion
- Pass environment variables to child processes
- Load `.env` files and keep secrets out of source code

## 2. Topic Explanation

**Environment variables** are key=value settings provided by the operating system to every process. They are the standard way to configure applications in containers and CI/CD (the [12-factor app](https://12factor.net/config) principle: *store config in the environment*).

```python
import os
db_host = os.environ.get("DB_HOST", "localhost")   # default if missing
api_key = os.environ["API_KEY"]                     # KeyError if missing (required)
```

Remember:
- Values are **always strings** → convert: `int(os.getenv("PORT", "8080"))`, booleans via `value.lower() in ("1", "true", "yes")`.
- `os.environ["X"] = "y"` changes the variable for the current process **and its children**, not for the parent shell.
- `subprocess.run(..., env={...})` gives a child process a custom environment.
- `.env` files hold local development settings. Load them with a small parser or the `python-dotenv` package. **Never commit real `.env` files** — commit `.env.example` instead.
- In Docker: `docker run -e DB_HOST=db`; in Kubernetes: `env:` / `envFrom:` with ConfigMaps and Secrets; in GitHub Actions: `env:` and `secrets.*`.

**Secrets** (passwords, tokens, AWS keys) must never be hard-coded. Read them from the environment or a secret manager.

## 3. Syntax

```python
import os
value = os.environ.get("NAME", "default")   # optional
value = os.getenv("NAME", "default")        # same thing
value = os.environ["NAME"]                  # required
os.environ["NAME"] = "value"                # set for this process + children
subprocess.run(cmd, env={**os.environ, "NAME": "value"})
```

| Part | Meaning |
|---|---|
| `os.environ` | Mapping of all environment variables. |
| `get / getenv` | Read with a default (returns a string or the default). |
| `os.environ["X"]` | Read a required variable (KeyError if missing). |
| `env={**os.environ, ...}` | Copy current env and override for a child process. |

## 4. Example 1 — Basic Example: Reading and converting environment variables

```python
import os

os.environ["APP_PORT"] = "9000"            # simulate values set by Docker/Kubernetes
os.environ["APP_DEBUG"] = "true"
os.environ["APP_WORKERS"] = "four"

port = int(os.getenv("APP_PORT", "8080"))
debug = os.getenv("APP_DEBUG", "false").lower() in ("1", "true", "yes")
region = os.getenv("AWS_REGION_DEMO", "us-east-1")
print("port:", port, type(port).__name__)
print("debug:", debug)
print("region (default used):", region)

try:
    workers = int(os.environ["APP_WORKERS"])
except ValueError:
    workers = 2
    print("APP_WORKERS is not a number - falling back to", workers)

try:
    secret = os.environ["DEMO_REQUIRED_SECRET"]
except KeyError:
    print("Missing required variable: DEMO_REQUIRED_SECRET")

app_vars = sorted(k for k in os.environ if k.startswith("APP_"))
print("APP_* variables:", app_vars)
```

## 5. Example 2 — Practical Example: A typed settings object loaded from env and a .env file

```python
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


def load_dotenv(path=".env"):
    """Tiny .env loader: KEY=value lines, comments and blanks ignored.
    Existing environment variables win (like python-dotenv's default)."""
    path = Path(path)
    if not path.exists():
        return 0
    loaded = 0
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
        loaded += 1
    return loaded


@dataclass
class Settings:
    env: str
    db_host: str
    db_port: int
    debug: bool
    db_password: str

    @classmethod
    def from_env(cls):
        missing = [k for k in ("DB_PASSWORD",) if k not in os.environ]
        if missing:
            raise RuntimeError(f"missing required environment variables: {missing}")
        return cls(
            env=os.getenv("APP_ENV", "dev"),
            db_host=os.getenv("DB_HOST", "localhost"),
            db_port=int(os.getenv("DB_PORT", "5432")),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            db_password=os.environ["DB_PASSWORD"],
        )

    def safe_repr(self):
        return f"Settings(env={self.env}, db={self.db_host}:{self.db_port}, debug={self.debug}, db_password=****)"


Path(".env").write_text('# local development only - never commit!\nAPP_ENV=dev\nDB_HOST=localhost\n'
                        'DB_PORT=5433\nDEBUG=true\nDB_PASSWORD="local-dev-password"\n')
os.environ["APP_ENV"] = "staging"          # already set -> .env must NOT override it

print("Loaded", load_dotenv(), "lines from .env")
settings = Settings.from_env()
print(settings.safe_repr())

child = subprocess.run(
    [sys.executable, "-c", "import os; print('child sees APP_ENV =', os.environ['APP_ENV'], '| FEATURE_X =', os.getenv('FEATURE_X'))"],
    env={**os.environ, "FEATURE_X": "on"}, capture_output=True, text=True,
)
print(child.stdout.strip())
print("parent sees FEATURE_X =", os.getenv("FEATURE_X"))
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- We set a few variables in code to simulate a container environment.
- `int(...)` and the `in ("1", "true", "yes")` check convert strings to proper types.
- A bad value (`"four"`) is caught and replaced with a safe default; a missing **required** variable is reported clearly.

**Example 2**
- `load_dotenv` reads `KEY=value` lines and uses `setdefault`, so real environment variables (e.g. set by Kubernetes) take priority over the file.
- `Settings.from_env` centralises all configuration: types are converted once, required values are validated at start-up (fail fast).
- `safe_repr` never prints the password.
- The child process receives `FEATURE_X` through `env=`; the parent's environment is unchanged.

## 7. Expected Output

**Example 1:**

```text
port: 9000 int
debug: True
region (default used): us-east-1
APP_WORKERS is not a number - falling back to 2
Missing required variable: DEMO_REQUIRED_SECRET
APP_* variables: ['APP_DEBUG', 'APP_PORT', 'APP_WORKERS']
```

**Example 2:**

```text
Loaded 5 lines from .env
Settings(env=staging, db=localhost:5433, debug=True, db_password=****)
child sees APP_ENV = staging | FEATURE_X = on
parent sees FEATURE_X = None
```

## 8. Common Mistakes

**1. Hard-coding secrets**

`password = "S3cret!"` in code ends up in Git history forever. Read it from the environment or a secret manager.

**2. Forgetting values are strings**

`if os.getenv("DEBUG"):` is True for the string `"false"`. Parse booleans explicitly.

**3. Expecting a script to change the parent shell**

`os.environ["X"] = ...` in Python does not change your terminal's environment. Use `export` in the shell or print the value for `eval`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Greeting from env:** Read `USER_NAME` from the environment (default `stranger`) and print `Hello, <name>!`. Run it once without and once after setting `os.environ["USER_NAME"]`.
- **Task 2 (Medium) — Typed config reader:** Write `env_int(name, default)` and `env_bool(name, default)` helpers that convert values and fall back to the default (with a warning) on invalid input. Test with `MAX_RETRIES=5`, `TIMEOUT=abc`, `VERBOSE=yes`.
- **Task 3 (Practical Challenge) — Config validator for a container:** Given a list of required variables `["DB_HOST", "DB_USER", "DB_PASSWORD", "REDIS_URL"]`, write `validate_env(required)` that returns missing names. Set some of them, print a start-up report that masks any variable containing `PASSWORD`, `SECRET` or `TOKEN`, and exit with code 1 (use `SystemExit`) if anything is missing — catch it in the solution to show the message.

## 10. DevOps/MLOps Connection

- **DevOps:** the same image runs in dev/staging/prod with different environment variables. CI systems inject credentials as masked env vars.
- **Cloud:** boto3 automatically reads `AWS_REGION`, `AWS_PROFILE`, `AWS_ACCESS_KEY_ID` from the environment (Day 82).
- **Kubernetes:** ConfigMaps and Secrets become env vars via `envFrom`.
- **MLOps:** model path, model version, thresholds and tracking URIs (`MLFLOW_TRACKING_URI`) are passed as env vars to training jobs and serving containers.

## 11. Interview Questions

**Q1. Why use environment variables for configuration?**

<details><summary>Show answer</summary>

They separate config from code, differ per environment without rebuilding, are supported by every platform, and keep secrets out of the repository.

</details>

**Q2. What type are environment variable values in Python?**

<details><summary>Show answer</summary>

Always strings (or None from getenv when missing).

</details>

**Q3. How do you pass extra environment variables to a subprocess without losing the existing ones?**

<details><summary>Show answer</summary>

`subprocess.run(cmd, env={**os.environ, "KEY": "value"})`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 67 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 066](../../07-devops-automation/day-066/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 068 ➡](../../07-devops-automation/day-068/README.md)
