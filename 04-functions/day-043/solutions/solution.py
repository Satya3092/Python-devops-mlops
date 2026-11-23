"""
Day 043 — Scope and Local/Global Variables: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
x = 10


def f():
    x = 20
    print(x)


f()
print(x)

# ===== Task 2 =====
deployments = 0


def deploy_global():
    global deployments
    deployments += 1


deploy_global()
deploy_global()
print("global version:", deployments)


def deploy(count):
    return count + 1


count = 0
count = deploy(count)
count = deploy(count)
print("pure version:", count)

# ===== Task 3 =====
DEFAULT_REGION = "ap-south-1"
ALLOWED_ENVS = ("dev", "staging", "prod")


def build_config(env, region=None):
    if env not in ALLOWED_ENVS:
        raise ValueError(f"env must be one of {ALLOWED_ENVS}, got {env!r}")
    return {"env": env, "region": region or DEFAULT_REGION}


print(build_config("prod"))
try:
    build_config("qa")
except ValueError as error:
    print("ValueError:", error)
