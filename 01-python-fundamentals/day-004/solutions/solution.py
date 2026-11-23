"""
Day 004 — Python Literals: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
requests_per_day = 86_400_000
max_file_size = 0xFFFF
file_permission = 0o644
print("Requests/day:", requests_per_day)
print("Max file size:", max_file_size)
print("Permission 0o644 in decimal:", file_permission)

# ===== Task 2 =====
print("SERVICE\tPORT\nnginx\t80\npostgres\t5432\nredis\t6379")

# ===== Task 3 =====
dockerfile = """FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]"""
print(dockerfile)
print("Lines:", dockerfile.count("\n") + 1)
