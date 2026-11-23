"""
run_examples.py - execute lesson examples and solutions (smoke test used in CI).

Examples that need user input get sample answers from the matching tasks.md /
README; network/AWS/Docker-dependent lessons are skipped by default.
Usage:
    python scripts/run_examples.py                 # all runnable days
    python scripts/run_examples.py --days 1 2 42   # specific days
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_INPUT = {5: 'Satya\nbilling-api\n2.4.1\nstaging\n', 6: '500\n412.5\n', 12: '87\n', 13: 'main\nno\n', 15: 'prod-db-01\n68\n32\n27.5\n500\n462\n'}
SOLUTION_INPUT = {5: 'Asha\nTerraform\nweb-01\n10.0.0.5\nUbuntu 24.04\nfeat\nauth\nadd token refresh\n', 6: '2.5\n4.7\n100\n', 12: '15\nadmin\n', 13: '42\n78\n4\n', 14: 'yellow\n62\n71\n93\n', 15: '2048\nravi\n17\nweb-07\n55\n200\n120\n9.6\n4\n', 30: 'hello\nadmin\ndevops123\n', 52: 'twenty\n'}
SKIP_BY_DEFAULT = {82: "needs AWS credentials + boto3", 98: "needs fastapi", 99: "needs Docker", 100: "needs Docker"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, nargs="*")
    parser.add_argument("--include-skipped", action="store_true")
    parser.add_argument("--solutions", action="store_true", help="also run solutions/solution.py")
    args = parser.parse_args()

    failures = []
    for day_dir in sorted(ROOT.glob("[0-9][0-9]-*/day-[0-9][0-9][0-9]")):
        n = int(day_dir.name[-3:])
        if args.days and n not in args.days:
            continue
        if n in SKIP_BY_DEFAULT and not args.include_skipped:
            print(f"Day {n:03d}: skipped ({SKIP_BY_DEFAULT[n]})")
            continue
        targets = ["examples.py"] + (["solutions/solution.py"] if args.solutions else [])
        for target in targets:
            stdin = (EXAMPLE_INPUT if target == "examples.py" else SOLUTION_INPUT).get(n, "")
            result = subprocess.run([sys.executable, target], cwd=day_dir, input=stdin, text=True,
                                    capture_output=True, timeout=180,
                                    env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", MPLBACKEND="Agg"))
            status = "ok" if result.returncode == 0 else "FAILED"
            print(f"Day {n:03d}: {target:<22} {status}")
            if result.returncode != 0:
                failures.append((n, target, result.stderr[-800:]))
    for n, target, err in failures:
        print(f"\n--- Day {n:03d} {target} ---\n{err}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
