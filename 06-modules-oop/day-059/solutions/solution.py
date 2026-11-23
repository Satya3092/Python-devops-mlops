"""
Day 059 — Pathlib Module: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
from pathlib import Path

# ===== Task 1 =====
p = Path("/home/ubuntu/projects/api/main.py")
print(p.name, p.stem, p.suffix, p.parent, p.parents[1], sep="\n")

# ===== Task 2 =====
root = Path("code_demo")
for rel in ["app/main.py", "app/utils/helpers.py", "tests/test_main.py", "README.md", "docs/guide.md"]:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# demo\n", encoding="utf-8")
for py in sorted(root.rglob("*.py")):
    print(py.relative_to(root).as_posix())

# ===== Task 3 =====
folder = Path("backups_demo")
folder.mkdir(exist_ok=True)
for day in range(15, 21):
    (folder / f"db-2026-11-{day}.sql.gz").write_text("dump", encoding="utf-8")
backups = sorted(folder.glob("db-*.sql.gz"), key=lambda p: p.name)   # ISO dates sort correctly
for old in backups[:-3]:
    old.unlink()
    print("Deleted:", old.name)
print("Remaining:", [p.name for p in sorted(folder.iterdir())])
