"""Small helper functions shared by several scripts (a custom module)."""

DEFAULT_THRESHOLD = 80


def percent(used, total):
    """Return used/total as a percentage rounded to 1 decimal."""
    return round(used / total * 100, 1) if total else 0.0


def status(value, threshold=DEFAULT_THRESHOLD):
    """Return 'ALERT' if value is above the threshold, otherwise 'OK'."""
    return "ALERT" if value > threshold else "OK"


if __name__ == "__main__":
    # Only runs when executing `python devops_utils.py`, not on import
    print("Self-test:", percent(40, 50), status(95))
