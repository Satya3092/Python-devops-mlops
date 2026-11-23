"""
Day 068 — Command-Line Arguments using argparse: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import argparse
from pathlib import Path

# ===== Task 1 =====
parser = argparse.ArgumentParser()
parser.add_argument("name")
parser.add_argument("--times", type=int, default=1)
args = parser.parse_args(["Asha", "--times", "3"])
for _ in range(args.times):
    print(f"Hello, {args.name}!")

# ===== Task 2 =====
scan = argparse.ArgumentParser(prog="scan.py")
scan.add_argument("host")
scan.add_argument("--ports", type=int, nargs="+", default=[22, 80, 443])
scan.add_argument("--timeout", type=float, default=1.0)
scan.add_argument("-v", "--verbose", action="store_true")
print(vars(scan.parse_args(["10.0.0.5"])))
print(vars(scan.parse_args(["db.internal", "--ports", "5432", "6379", "--timeout", "0.5", "-v"])))

# ===== Task 3 =====
def count(args):
    lines = Path(args.file).read_text().splitlines()
    return f"{args.level}: {sum(1 for l in lines if f' {args.level} ' in l)} lines"


def tail(args):
    return "\n".join(Path(args.file).read_text().splitlines()[-args.n:])


def search(args):
    pattern = args.pattern.lower() if args.ignore_case else args.pattern
    lines = Path(args.file).read_text().splitlines()
    hits = [l for l in lines if pattern in (l.lower() if args.ignore_case else l)]
    return "\n".join(hits) or "no matches"


tool = argparse.ArgumentParser(prog="logtool")
sub = tool.add_subparsers(dest="command", required=True)
p = sub.add_parser("count")
p.add_argument("file")
p.add_argument("--level", choices=["INFO", "WARNING", "ERROR"], default="ERROR")
p.set_defaults(func=count)
p = sub.add_parser("tail")
p.add_argument("file")
p.add_argument("-n", type=int, default=5)
p.set_defaults(func=tail)
p = sub.add_parser("search")
p.add_argument("file")
p.add_argument("pattern")
p.add_argument("--ignore-case", action="store_true")
p.set_defaults(func=search)

LOG = "../../datasets/app.log"
for argv in (["count", LOG, "--level", "ERROR"], ["tail", LOG, "-n", "3"],
             ["search", LOG, "DATABASE", "--ignore-case"]):
    args = tool.parse_args(argv)
    print(f"$ logtool {args.command} ...")
    print(args.func(args))
