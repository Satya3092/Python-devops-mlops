"""
Day 054 — Creating Custom Exceptions: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
def validate_email(email):
    if "@" not in email:
        raise ValueError(f"{email!r}: missing @")
    if "." not in email.split("@")[1]:
        raise ValueError(f"{email!r}: domain has no dot")
    return True


for e in ["asha@example.com", "ravi.example.com", "meera@localhost"]:
    try:
        validate_email(e)
        print(e, "is valid")
    except ValueError as error:
        print("Invalid:", error)

# ===== Task 2 =====
class QuotaExceededError(Exception):
    """Raised when a resource request exceeds the account limit."""


def request_instances(current, requested, limit=20):
    if current + requested > limit:
        raise QuotaExceededError(f"requested {requested}, but only {limit - current} of {limit} available")
    return current + requested


for current, requested in [(10, 5), (18, 4)]:
    try:
        print("New total:", request_instances(current, requested))
    except QuotaExceededError as error:
        print("Quota error:", error)

# ===== Task 3 =====
class BackupError(Exception):
    """Base error for the backup tool."""


class SourceMissingError(BackupError):
    """The source directory does not exist."""


class InsufficientSpaceError(BackupError):
    def __init__(self, needed_gb, free_gb):
        super().__init__(f"need {needed_gb} GB, only {free_gb} GB free")
        self.needed_gb = needed_gb
        self.free_gb = free_gb


EXISTING = {"/var/lib/postgresql", "/etc"}


def backup(source, size_gb, free_gb):
    if source not in EXISTING:
        raise SourceMissingError(f"{source} does not exist")
    if size_gb > free_gb:
        raise InsufficientSpaceError(size_gb, free_gb)
    return f"backed up {source} ({size_gb} GB)"


for args in [("/etc", 1, 50), ("/data", 5, 50), ("/var/lib/postgresql", 120, 80)]:
    try:
        print(backup(*args))
    except InsufficientSpaceError as error:
        print(f"Space problem: {error}. Free at least {error.needed_gb - error.free_gb} GB.")
    except BackupError as error:
        print(f"{type(error).__name__}: {error}")
