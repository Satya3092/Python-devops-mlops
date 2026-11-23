"""
Day 039 — Default Arguments: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
def power(base, exponent=2):
    return base ** exponent


print(power(5))
print(power(2, 10))

# ===== Task 2 =====
def backup_name(db, date="2026-11-20", ext="sql.gz"):
    return f"{db}-{date}.{ext}"


print(backup_name("orders"))
print(backup_name("orders", "2026-12-01"))
print(backup_name("users", ext="dump"))

# ===== Task 3 =====
def describe_request(url, method="GET", headers=None, timeout=5, retries=3):
    final_headers = {"User-Agent": "devops-script/1.0"}
    if headers:
        final_headers.update(headers)
    return (f"{method} {url}\n"
            f"  headers: {final_headers}\n"
            f"  timeout: {timeout}s, retries: {retries}")


my_headers = {"Accept": "application/json"}
print(describe_request("https://api.example.com/health"))
print(describe_request("https://api.example.com/orders", "POST", my_headers, timeout=10))
print("Caller's headers unchanged:", my_headers)
