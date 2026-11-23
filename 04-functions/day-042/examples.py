"""
Day 042 — Variable-Length Arguments (**kwargs)
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Collecting keyword arguments
# ======================================================================
def show_profile(name, **details):
    print("Name:", name)
    for key, value in details.items():
        print(f"  {key}: {value}")


show_profile("Asha", city="Pune", role="DevOps Engineer", years=6)
show_profile("Ravi")

extra = {"language": "Python", "level": "beginner"}
show_profile("Meera", **extra)


def everything(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)


everything(1, 2, mode="fast", retries=3)

# ======================================================================
# Example 2 — Configuration-driven resource creation
# ======================================================================
def create_bucket(name, region="us-east-1", **tags):
    """Simulate creating an S3 bucket with any number of tags."""
    tag_text = ", ".join(f"{k}={v}" for k, v in sorted(tags.items())) or "no tags"
    return f"Bucket '{name}' in {region} [{tag_text}]"


# Config as it might be loaded from a YAML file
buckets_config = [
    {"name": "app-logs", "region": "ap-south-1", "Env": "prod", "Owner": "platform"},
    {"name": "ml-datasets", "Project": "churn-model", "Env": "dev"},
    {"name": "tmp-scratch"},
]
for config in buckets_config:
    print(create_bucket(**config))


def with_logging(func, *args, **kwargs):
    """Call any function, logging its arguments first (a simple wrapper)."""
    print(f"-> calling {func.__name__} args={args} kwargs={kwargs}")
    result = func(*args, **kwargs)
    print(f"<- {func.__name__} returned: {result}")
    return result


with_logging(create_bucket, "audit-trail", region="eu-west-1", Compliance="SOC2")
