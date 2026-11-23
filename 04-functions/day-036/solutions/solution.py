"""
Day 036 — Introduction to Functions: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
def say_hello():
    """Introduce the course."""
    print("Hello!")
    print("Welcome to 100 Days of Python.")
    print("From beginner to MLOps.")


say_hello()
say_hello()

# ===== Task 2 =====
def print_separator():
    """Print a line of 40 dashes."""
    print("-" * 40)


print_separator()
print("Linux: everything is a file")
print_separator()
print("Docker: containers share the host kernel")
print_separator()
print("Kubernetes: the smallest deployable unit is a pod")
print_separator()

# ===== Task 3 =====
def pull_code():
    """Get the latest code."""
    print("[1/4] Pulling latest code from main")


def run_tests():
    """Run the unit tests."""
    print("[2/4] Running unit tests")


def build_image():
    """Build the Docker image."""
    print("[3/4] Building Docker image")


def deploy():
    """Deploy to the cluster."""
    print("[4/4] Deploying to Kubernetes")


def main():
    """Run the pipeline steps in order."""
    pull_code()
    run_tests()
    build_image()
    deploy()
    print("Deployment pipeline finished")


main()
