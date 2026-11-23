"""
Day 023 — List Methods
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Exploring list methods
# ======================================================================
queue = ["job-1", "job-2"]
queue.append("job-3")
queue.extend(["job-4", "job-5"])
queue.insert(0, "urgent-job")
print("Queue:", queue)

next_job = queue.pop(0)          # FIFO: take from the front
print("Processing:", next_job)
last_job = queue.pop()           # take from the end
print("Removed from end:", last_job)
print("Queue now:", queue)

print("Index of job-3:", queue.index("job-3"))
versions = [3, 1, 2, 3, 3]
print("Count of 3:", versions.count(3))
versions.sort()
print("Sorted:", versions)
versions.reverse()
print("Reversed:", versions)

# ======================================================================
# Example 2 — Docker image cleanup planner
# ======================================================================
images = ["app:1.0.3", "app:1.0.10", "app:1.0.1", "app:1.0.7", "app:1.0.9", "app:1.0.2"]
KEEP_LATEST = 3

def version_key(image):                    # functions are covered on Day 36
    version = image.split(":")[1]          # "1.0.10"
    return [int(part) for part in version.split(".")]

print("Text sort (wrong):", sorted(images))
images.sort(key=version_key, reverse=True)  # newest first, numeric order
print("Version sort:", images)

to_keep = images[:KEEP_LATEST]
to_delete = images[KEEP_LATEST:]
print("Keep:", to_keep)
print("Delete:", to_delete)

deleted = []
while to_delete:                            # while loops: Day 30
    image = to_delete.pop()
    deleted.append(image)
    print(f"docker rmi {image}")
print("Deleted", len(deleted), "images")
