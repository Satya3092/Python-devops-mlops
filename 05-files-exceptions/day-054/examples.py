"""
Day 054 — Creating Custom Exceptions
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Raising built-in and custom exceptions
# ======================================================================
def set_replicas(count):
    if not isinstance(count, int):
        raise TypeError("replicas must be an integer")
    if count < 0:
        raise ValueError("replicas cannot be negative")
    return f"Scaled to {count} replicas"


for value in (3, -1, "two"):
    try:
        print(set_replicas(value))
    except (TypeError, ValueError) as error:
        print(f"{type(error).__name__}: {error}")


class InsufficientFundsError(Exception):
    """Raised when an account balance is too low."""


try:
    raise InsufficientFundsError("balance 100, requested 250")
except InsufficientFundsError as error:
    print("Custom error caught:", error)

# ======================================================================
# Example 2 — An exception hierarchy for a deployment tool
# ======================================================================
class DeployToolError(Exception):
    """Base class for every error raised by our deployment tool."""


class ConfigError(DeployToolError):
    """The deployment configuration is invalid."""


class HealthCheckError(DeployToolError):
    """A host failed its health check after deployment."""

    def __init__(self, host, status_code):
        super().__init__(f"{host} returned HTTP {status_code}")
        self.host = host
        self.status_code = status_code


def validate_config(config):
    for key in ("service", "version", "hosts"):
        if key not in config:
            raise ConfigError(f"missing required key '{key}'")
    if not config["hosts"]:
        raise ConfigError("at least one host is required")


def deploy(config, health):
    validate_config(config)
    for host in config["hosts"]:
        status = health.get(host, 200)
        if status != 200:
            raise HealthCheckError(host, status)
        print(f"  {host}: deployed {config['service']} {config['version']}")
    return "success"


scenarios = [
    ({"service": "orders", "version": "1.2", "hosts": ["web-01", "web-02"]}, {}),
    ({"service": "orders", "hosts": ["web-01"]}, {}),
    ({"service": "orders", "version": "1.3", "hosts": ["web-01", "web-02"]}, {"web-02": 503}),
]
for config, health in scenarios:
    print("Deploying", config)
    try:
        print("Result:", deploy(config, health))
    except HealthCheckError as error:
        print(f"Rollback needed! host={error.host} code={error.status_code}")
    except DeployToolError as error:
        print(f"{type(error).__name__}: {error}")
