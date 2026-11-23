"""
Day 053 — try, except, else, finally: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
def check(value):
    try:
        number = int(value)
    except ValueError:
        print("invalid")
    else:
        print("valid:", number)
    finally:
        print("checked")


check("7")
check("x")

# ===== Task 2 =====
def run_query(conn, query):
    try:
        if "DROP" in query.upper():
            raise ValueError("dangerous query blocked")
        print("Executed:", query)
    finally:
        conn["open"] = False


for q in ["SELECT * FROM orders", "drop table orders"]:
    connection = {"open": True}
    try:
        run_query(connection, q)
    except ValueError as error:
        print("Error:", error)
    print("open:", connection["open"])

# ===== Task 3 =====
def fetch_with_retry(results, max_attempts=3):
    attempts = 0
    last_error = None
    for attempt in range(max_attempts):
        try:
            if not results[attempt]:
                raise ConnectionError(f"attempt {attempt + 1} failed")
        except ConnectionError as error:
            last_error = error
            print("retrying:", error)
        else:
            print(f"success after {attempts + 1} attempts")
            return True
        finally:
            attempts += 1
    raise last_error


fetch_with_retry([False, True, True])
try:
    fetch_with_retry([False, False, False])
except ConnectionError as error:
    print("Gave up:", error)
