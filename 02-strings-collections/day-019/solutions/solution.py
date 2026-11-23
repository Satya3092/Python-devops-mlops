"""
Day 019 — String Methods: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
env = "  StAgInG \n"
clean_env = env.strip().lower()
print(clean_env)
print("Valid:", clean_env in ("dev", "staging", "prod"))

# ===== Task 2 =====
line = "DB_HOST=db.internal; DB_PORT=5432; DB_NAME=orders"
for pair in line.split(";"):
    key, value = pair.strip().split("=")
    print(key, "->", value)

# ===== Task 3 =====
ps_line = "www-data  1234  12.5  3.1  456789  65432 ?  S  10:01  0:42 nginx: worker process"
fields = ps_line.split(maxsplit=10)
user, pid, cpu, mem = fields[0], fields[1], float(fields[2]), float(fields[3])
command = fields[10]
print("User:", user, "| PID:", pid, "| CPU:", cpu, "| MEM:", mem)
print("Command:", command)
if cpu > 10:
    print("FLAG: high CPU process ->", pid)
