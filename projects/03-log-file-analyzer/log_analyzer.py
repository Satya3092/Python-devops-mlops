"""
Project 3 - Log File Analyzer.

Usage:
    python log_analyzer.py PATH [PATH ...] [--top N] [--json] [--fail-on-errors N]
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

LEVELS = ("INFO", "WARNING", "ERROR")
LINE_PATTERN = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<level>[A-Z]+) (?P<message>.*)$")
NUMBERS = re.compile(r"\d+")


class LogParseError(Exception):
    """Raised when a line does not follow 'YYYY-MM-DD HH:MM:SS LEVEL message'."""


def parse_line(line):
    match = LINE_PATTERN.match(line.strip())
    if not match or match["level"] not in LEVELS:
        raise LogParseError(line.strip()[:60])
    return match.groupdict()


def normalise(message):
    """Group similar messages: 'timeout after 2418ms' -> 'timeout after <N>ms'."""
    message = re.sub(r"\[[\d.]+\]\s*", "", message)          # drop "[10.0.0.5]" client IPs
    return NUMBERS.sub("<N>", message).strip()


def collect_files(paths):
    files, problems = [], []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(path.glob("*.log")))
        elif path.is_file():
            files.append(path)
        else:
            problems.append(f"{raw}: no such file or directory")
    return files, problems


def analyse_file(path):
    stats = {"file": path.name, "lines": 0, "bad": 0, **{level: 0 for level in LEVELS}}
    errors, per_minute = Counter(), Counter()
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip():
                continue
            stats["lines"] += 1
            try:
                entry = parse_line(line)
            except LogParseError:
                stats["bad"] += 1
                continue
            stats[entry["level"]] += 1
            if entry["level"] == "ERROR":
                errors[normalise(entry["message"])] += 1
                per_minute[f"{entry['date']} {entry['time'][:5]}"] += 1
    return stats, errors, per_minute


def analyse(paths, top=3):
    files, problems = collect_files(paths)
    report = {"files": [], "totals": {level: 0 for level in LEVELS}, "bad_lines": 0,
              "top_errors": [], "busiest_error_minute": None, "problems": problems}
    all_errors, all_minutes = Counter(), Counter()
    for path in files:
        try:
            stats, errors, minutes = analyse_file(path)
        except OSError as error:                       # permission denied, etc.
            report["problems"].append(f"{path}: {error.strerror}")
            continue
        report["files"].append(stats)
        for level in LEVELS:
            report["totals"][level] += stats[level]
        report["bad_lines"] += stats["bad"]
        all_errors.update(errors)
        all_minutes.update(minutes)
    valid = sum(report["totals"].values())
    report["error_rate_percent"] = round(report["totals"]["ERROR"] / valid * 100, 1) if valid else 0.0
    report["top_errors"] = all_errors.most_common(top)
    if all_minutes:
        minute, count = all_minutes.most_common(1)[0]
        report["busiest_error_minute"] = {"minute": minute, "errors": count}
    return report


def print_report(report):
    print(f"{'FILE':<16}{'LINES':>6}{'INFO':>7}{'WARNING':>9}{'ERROR':>7}{'BAD':>5}")
    for s in report["files"]:
        print(f"{s['file']:<16}{s['lines']:>6}{s['INFO']:>7}{s['WARNING']:>9}{s['ERROR']:>7}{s['bad']:>5}")
    t = report["totals"]
    print(f"{'TOTAL':<16}{sum(s['lines'] for s in report['files']):>6}{t['INFO']:>7}{t['WARNING']:>9}"
          f"{t['ERROR']:>7}{report['bad_lines']:>5}")
    print(f"\nError rate: {report['error_rate_percent']}% of valid lines")
    print("Top errors:")
    for message, count in report["top_errors"]:
        print(f"  {count} x {message}")
    if report["busiest_error_minute"]:
        b = report["busiest_error_minute"]
        print(f"Busiest error minute: {b['minute']} ({b['errors']} errors)")
    for problem in report["problems"]:
        print("WARNING:", problem, file=sys.stderr)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Count INFO/WARNING/ERROR lines in log files.")
    parser.add_argument("paths", nargs="+", help="log files or folders")
    parser.add_argument("--top", type=int, default=3, help="number of top errors to show")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a table")
    parser.add_argument("--fail-on-errors", type=int, metavar="N", help="exit 1 if total errors >= N")
    args = parser.parse_args(argv)

    report = analyse(args.paths, top=args.top)
    if not report["files"]:
        print("No log files found.", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report)
    if args.fail_on_errors is not None and report["totals"]["ERROR"] >= args.fail_on_errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
