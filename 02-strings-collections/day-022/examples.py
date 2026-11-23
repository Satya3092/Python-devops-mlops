"""
Day 022 — List Indexing and Slicing
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Indexing and slicing a list
# ======================================================================
regions = ["us-east-1", "us-west-2", "eu-west-1", "ap-south-1", "ap-northeast-1"]
print("First:", regions[0])
print("Last:", regions[-1])
print("First two:", regions[:2])
print("Last two:", regions[-2:])
print("Every other:", regions[::2])
print("Reversed:", regions[::-1])

regions[1] = "us-west-1"
del regions[2]
print("Modified:", regions)

# ======================================================================
# Example 2 — Tail of a log and batch processing
# ======================================================================
log_lines = [f"line {n}: request served" for n in range(1, 13)]   # 12 fake lines

# Like 'tail -3'
print("Last 3 lines:")
for line in log_lines[-3:]:
    print("  ", line)

# Process hosts in batches of 4 (rolling deployment!)
hosts = [f"web-{n:02d}" for n in range(1, 11)]
batch_size = 4
for start in range(0, len(hosts), batch_size):
    batch = hosts[start:start + batch_size]
    print(f"Deploying batch starting at {start}: {batch}")

# Canary: deploy to the first host only, rest later
canary, remaining = hosts[0], hosts[1:]
print("Canary:", canary, "| remaining:", len(remaining))
