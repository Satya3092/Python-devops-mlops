"""
Day 002 — Variables and Naming Conventions: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
full_name = "Satya Prakash Singh"
city = "Bengaluru"
years_experience = 10
favourite_tool = "Kubernetes"
print("Name:", full_name)
print("City:", city)
print("Experience (years):", years_experience)
print("Favourite tool:", favourite_tool)

# ===== Task 2 =====
primary_db = "db-01"
replica_db = "db-02"
print("Before -> primary:", primary_db, "| replica:", replica_db)
primary_db, replica_db = replica_db, primary_db
print("After  -> primary:", primary_db, "| replica:", replica_db)

# ===== Task 3 =====
REGISTRY = "docker.io"
image_name = "nginx"
image_tag = "1.27"
container_name = "web"
host_port = 8080
container_port = 80
restart_policy = "always"
print("Image:", REGISTRY + "/" + image_name + ":" + image_tag)
print("Container:", container_name)
print("Ports:", host_port, "->", container_port)
print("Command:")
print("docker run -d --name", container_name, "-p", str(host_port) + ":" + str(container_port),
      "--restart", restart_policy, REGISTRY + "/" + image_name + ":" + image_tag)
