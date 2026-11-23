"""
Day 040 — Keyword Arguments
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Positional vs keyword calls
# ======================================================================
def describe_pet(animal, name, age=1):
    return f"{name} is a {age}-year-old {animal}"


print(describe_pet("cat", "Milo"))
print(describe_pet(name="Bruno", animal="dog", age=4))
print(describe_pet("parrot", age=12, name="Rio"))

# describe_pet(name="Kitty", "cat")   # SyntaxError: positional argument follows keyword argument

# ======================================================================
# Example 2 — Safe, self-documenting infrastructure helpers
# ======================================================================
def create_instance(name, instance_type="t3.micro", *, region="us-east-1",
                    env="dev", monitoring=False, dry_run=True):
    """Describe an EC2 instance launch; region and flags are keyword-only."""
    mode = "DRY RUN" if dry_run else "LAUNCH"
    return (f"[{mode}] {name} type={instance_type} region={region} "
            f"env={env} monitoring={'on' if monitoring else 'off'}")


print(create_instance("web-01"))
print(create_instance("db-01", "m5.large", region="ap-south-1", env="prod", monitoring=True))
print(create_instance("batch-01", dry_run=False))

try:
    create_instance("web-02", "t3.small", "eu-west-1")   # region passed positionally
except TypeError as error:
    print("TypeError:", error)
