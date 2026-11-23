"""
validate_repo.py - structural checks for the course (used in CI).

Checks: exactly 100 day folders; required files; all 12 lesson sections; >= 3 tasks
with expected outputs; solutions with 3 task markers; Python files compile;
relative Markdown links resolve.
Run: python scripts/validate_repo.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ["## 1. Learning Objectives", "## 2. Topic Explanation", "## 3. Syntax",
            "## 4. Example 1", "## 5. Example 2", "## 6. Code Explanation", "## 7. Expected Output",
            "## 8. Common Mistakes", "## 9. Practice Tasks", "## 10. DevOps/MLOps Connection",
            "## 11. Interview Questions", "## 12. Day Completion Checklist"]
LINK = re.compile(r"\]\((?!https?://|mailto:|#)([^)#\s]+)(?:#[^)]*)?\)")


def main():
    errors = []
    days = sorted(ROOT.glob("[0-9][0-9]-*/day-[0-9][0-9][0-9]"))
    numbers = [int(d.name[-3:]) for d in days]
    if numbers != list(range(1, 101)):
        errors.append(f"expected days 1..100, found {len(numbers)} folders")
    for day in days:
        for required in ("README.md", "examples.py", "tasks.md", "solutions/solution.py"):
            if not (day / required).exists():
                errors.append(f"{day.relative_to(ROOT)}: missing {required}")
        readme = (day / "README.md").read_text(encoding="utf-8")
        for section in SECTIONS:
            if section not in readme:
                errors.append(f"{day.name}: missing section '{section}'")
        syntax_part = readme.split("## 3. Syntax", 1)[-1].split("## 4.", 1)[0]
        if "```" not in syntax_part or readme.count("```python") < 2:
            errors.append(f"{day.name}: expected a syntax block and 2 Python examples")
        tasks = (day / "tasks.md").read_text(encoding="utf-8")
        if tasks.count("## Task ") < 3 or tasks.count("**Expected output:**") < 3:
            errors.append(f"{day.name}: needs >= 3 tasks with expected output")
        solution = (day / "solutions" / "solution.py").read_text(encoding="utf-8")
        if len(re.findall(r"^# ===== Task \d", solution, re.M)) < 3:
            errors.append(f"{day.name}: solution needs 3 task sections")
    for py in ROOT.rglob("*.py"):
        if ".venv" in py.parts:
            continue
        try:
            compile(py.read_text(encoding="utf-8"), str(py), "exec")
        except SyntaxError as error:
            errors.append(f"syntax error: {py.relative_to(ROOT)}:{error.lineno}: {error.msg}")
    for md in ROOT.rglob("*.md"):
        if ".venv" in md.parts:
            continue
        for target in LINK.findall(md.read_text(encoding="utf-8")):
            if not (md.parent / target).exists():
                errors.append(f"broken link in {md.relative_to(ROOT)} -> {target}")
    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} problem(s) found")
        return 1
    print(f"OK: {len(days)} lessons, all sections present, all Python files compile, all relative links resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
