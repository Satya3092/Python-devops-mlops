"""
Day 067 — Working with Environment Variables
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Reading and converting environment variables
# ======================================================================
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

# ======================================================================
# Example 2 — A typed settings object loaded from env and a .env file
# ======================================================================
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
