"""
Day 005 — Input and Output: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
name = input("Your name: ")
tool = input("Favourite DevOps tool: ")
print()
print("Hi ", name, "! ", tool, " is a great choice.", sep="")

# ===== Task 2 =====
hostname = input("Hostname: ")
ip_address = input("IP: ")
operating_system = input("OS: ")
print()
print(hostname, ip_address, operating_system, sep=",")

# ===== Task 3 =====
change_type = input("Type (feat/fix/docs): ")
scope = input("Scope: ")
message = input("Message: ")
commit_message = change_type + "(" + scope + "): " + message
print()
print("Commit message:", commit_message)
print('git commit -m "', commit_message, '"', sep="")
