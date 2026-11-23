"""
Day 037 — Function Parameters and Arguments: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
def print_area(width, height):
    print("Area:", width * height)


print_area(5, 3)
print_area(12, 7)

# ===== Task 2 =====
def print_ssh_command(user, host, port):
    print(f"ssh -p {port} {user}@{host}")


print_ssh_command("ubuntu", "10.0.0.5", 22)
print_ssh_command("ec2-user", "bastion.example.com", 2222)
print_ssh_command("admin", "db-01.internal", 22)

# ===== Task 3 =====
def log(level, service, message):
    print(f"[{level.upper():<7}] {service}: {message}")


def log_many(level, service, messages):
    for message in messages:
        log(level, service, message)


log("info", "auth", "user logged in")
log("error", "payments", "card declined")
log_many("warning", "orders", ["slow query", "retrying request"])
