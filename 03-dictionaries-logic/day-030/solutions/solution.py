"""
Day 030 — While Loops: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
number = 98765
digit_sum = 0
while number > 0:
    digit_sum += number % 10
    number //= 10
print("Sum of digits:", digit_sum)

# ===== Task 2 =====
CORRECT = "devops123"
attempts = 0
granted = False
while attempts < 3 and not granted:
    password = input("Password: ")
    attempts += 1
    if password == CORRECT:
        granted = True
    else:
        print("Wrong password")
print("Access granted" if granted else "Account locked")

# ===== Task 3 =====
queue = ["order-1", "order-2", "POISON", "order-3"]
processed = []
dead_letter = []
while queue:
    message = queue.pop(0)
    if message == "POISON":
        dead_letter.append(message)
        print("Moved to dead-letter queue:", message)
    else:
        processed.append(message)
        print("Processed:", message)
print("Processed:", processed)
print("Dead letter:", dead_letter)
