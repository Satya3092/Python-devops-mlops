"""
Day 053 — try, except, else, finally
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Seeing the flow
# ======================================================================
def divide(a, b):
    print(f"--- divide({a}, {b}) ---")
    try:
        result = a / b
    except ZeroDivisionError:
        print("except: cannot divide by zero")
        return None
    else:
        print("else: success, result =", result)
        return result
    finally:
        print("finally: always runs")


print("Returned:", divide(10, 2))
print("Returned:", divide(1, 0))

# ======================================================================
# Example 2 — A deployment with a lock file and guaranteed cleanup
# ======================================================================
import os

LOCK_FILE = "deploy.lock"


def deploy(version, fail=False):
    if os.path.exists(LOCK_FILE):
        print("Another deployment is running - abort")
        return False

    open(LOCK_FILE, "w").close()                     # create the lock
    print(f"Deploying {version} (lock acquired)")
    try:
        if fail:
            raise RuntimeError("health check failed after rollout")
        print("Rollout complete")
    except RuntimeError as error:
        print("Deployment error:", error)
        print("Rolling back...")
        return False
    else:
        print("Recording successful release", version)
        return True
    finally:
        os.remove(LOCK_FILE)                         # ALWAYS release the lock
        print("Lock released")


print("Result:", deploy("v1.2.0"))
print()
print("Result:", deploy("v1.3.0", fail=True))
print("Lock left behind?", os.path.exists(LOCK_FILE))
