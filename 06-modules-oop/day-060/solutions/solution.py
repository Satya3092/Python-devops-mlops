"""
Day 060 — Shutil Module: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import shutil
from pathlib import Path

# ===== Task 1 =====
Path("nginx.conf").write_text("worker_processes auto;\n")
shutil.copy2("nginx.conf", "nginx.conf.bak")
print(Path("nginx.conf").stat().st_size, Path("nginx.conf.bak").stat().st_size)

# ===== Task 2 =====
folder = Path("report_files")
folder.mkdir(exist_ok=True)
for i in range(1, 4):
    (folder / f"report{i}.txt").write_text(f"report {i}\n")
shutil.make_archive("reports", "zip", root_dir=folder)
shutil.unpack_archive("reports.zip", "restored")
print(sorted(p.name for p in Path("restored").iterdir()))

# ===== Task 3 =====
def disk_report(path="."):
    total, used, free = shutil.disk_usage(path)
    gb = 1024 ** 3
    report = {
        "total_gb": round(total / gb, 2),
        "used_gb": round(used / gb, 2),
        "free_gb": round(free / gb, 2),
        "used_percent": round(used / total * 100, 1),
    }
    if report["used_percent"] > 80:
        print("WARNING: disk usage above 80%")
    return report


print(disk_report())
for tool in ["git", "tar", "terraform"]:
    print(f"{tool:<10} {'OK' if shutil.which(tool) else 'MISSING'}")
