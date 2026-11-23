"""
Day 052 — Exception Handling: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import json

# ===== Task 1 =====
age_text = input("Age: ")
try:
    age = int(age_text)
    print("Next year you will be", age + 1)
except ValueError:
    print("Please enter a whole number")

# ===== Task 2 =====
def get_item(items, index):
    try:
        return items[index]
    except IndexError:
        return "out of range"


letters = ["a", "b", "c"]
for i in (0, 5, -1):
    print(i, get_item(letters, i))

# ===== Task 3 =====
def load_port(path):
    try:
        with open(path, encoding="utf-8") as f:
            config = json.load(f)
        return int(config["server"]["port"])
    except FileNotFoundError:
        print(f"{path}: file not found")
    except json.JSONDecodeError as error:
        print(f"{path}: invalid JSON ({error.msg})")
    except KeyError as error:
        print(f"{path}: missing key {error}")
    except ValueError:
        print(f"{path}: port is not a number")
    return None


files = {
    "good.json": '{"server": {"port": "8080"}}',
    "broken.json": '{"server": {"port": 8080,}}',
    "nokey.json": '{"server": {}}',
    "badport.json": '{"server": {"port": "http"}}',
}
for name, content in files.items():
    with open(name, "w", encoding="utf-8") as f:
        f.write(content)
for name in ["good.json", "missing.json", "broken.json", "nokey.json", "badport.json"]:
    print(name, "->", load_port(name))
