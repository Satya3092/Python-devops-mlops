"""
Day 040 — Keyword Arguments: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
def order_pizza(size, crust="thin", extra_cheese=False):
    cheese = "with extra cheese" if extra_cheese else "regular cheese"
    return f"{size} pizza, {crust} crust, {cheese}"


print(order_pizza("large"))
print(order_pizza(extra_cheese=True, size="medium"))
print(order_pizza(crust="stuffed", size="small"))

# ===== Task 2 =====
def scale_command(deployment, *, replicas, namespace="default"):
    return f"kubectl scale deployment/{deployment} --replicas={replicas} -n {namespace}"


print(scale_command("api", replicas=5))
print(scale_command("worker", replicas=2, namespace="jobs"))
try:
    scale_command("api", 5)
except TypeError as error:
    print("TypeError:", error)

# ===== Task 3 =====
def delete_old_backups(backups, *, keep=3, dry_run=True):
    to_delete = backups[:-keep] if keep > 0 else backups[:]
    for name in to_delete:
        print(("Would delete " if dry_run else "Deleting ") + name)
    return to_delete


backups = ["db-11-15.gz", "db-11-16.gz", "db-11-17.gz", "db-11-18.gz", "db-11-19.gz"]
print(delete_old_backups(backups))
print(delete_old_backups(backups, keep=4, dry_run=False))
