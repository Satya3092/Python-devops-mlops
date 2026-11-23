"""
Day 022 — List Indexing and Slicing: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
numbers = list(range(1, 21))
print(numbers[:5])
print(numbers[-5:])
print(numbers[5:15])

# ===== Task 2 =====
stages = ["build", "test", "deploy-dev", "deploy-prod"]
stages[1:2] = ["security-scan", "integration-test"]
del stages[stages.index("deploy-dev")]
print(stages)

# ===== Task 3 =====
pods = [f"pod-{n}" for n in range(1, 12)]
wave_size = max(1, len(pods) * 25 // 100)
waves = 0
for start in range(0, len(pods), wave_size):
    waves += 1
    print(f"Wave {waves}: {pods[start:start + wave_size]}")
print("Total waves:", waves)
