"""
Day 011 — Operator Precedence: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
print(5 + 2 * 3 - 1)
print((5 + 2) * (3 - 1))
print(20 / 4 / 5)
print(2 ** 2 ** 3)

# ===== Task 2 =====
f = 98.6
wrong_c = f - 32 * 5 / 9
right_c = (f - 32) * 5 / 9
print("Wrong:", round(wrong_c, 1))
print("Right:", round(right_c, 1))

# ===== Task 3 =====
cpu, memory, disk = 80, 60, 50
score = 100 - (cpu * 0.4 + memory * 0.4 + disk * 0.2)
print("Health score:", score)
needs_attention = score < 40 or cpu > 90 and memory > 90
needs_attention_explicit = (score < 40) or ((cpu > 90) and (memory > 90))
print("Needs attention:", needs_attention)
print("Needs attention (explicit):", needs_attention_explicit)
