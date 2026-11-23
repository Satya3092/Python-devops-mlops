"""
Day 055 — File Processing Automation Project
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Parsing one line with a custom exception
# ======================================================================
class ParseError(Exception):
    """Raised when a log line does not match the expected format."""


LEVELS = {"INFO", "WARNING", "ERROR"}


def parse_line(line):
    """Return a dict for a log line or raise ParseError."""
    parts = line.split()
    if len(parts) < 4 or parts[2] not in LEVELS:
        raise ParseError(f"unexpected format: {line.strip()!r}")
    fields = {}
    message_words = []
    for word in parts[3:]:
        if "=" in word:
            key, value = word.split("=", 1)
            fields[key] = value
        else:
            message_words.append(word)
    return {
        "timestamp": f"{parts[0]} {parts[1]}",
        "level": parts[2],
        "message": " ".join(message_words),
        "fields": fields,
    }


print(parse_line("2026-11-20 10:00:09 ERROR Database timeout path=/api/orders ms=5000"))
try:
    parse_line("this line is corrupted")
except ParseError as error:
    print("ParseError:", error)

# ======================================================================
# Example 2 — Project — Log Folder Processor
# ======================================================================
import csv
import json
import os


class ParseError(Exception):
    """Raised when a log line does not match the expected format."""


LEVELS = ("INFO", "WARNING", "ERROR")


def find_log_files(folder):
    """Return sorted paths of *.log files in a folder."""
    try:
        names = sorted(os.listdir(folder))
    except FileNotFoundError:
        print(f"Folder not found: {folder}")
        return []
    return [os.path.join(folder, n) for n in names if n.endswith(".log")]


def parse_line(line):
    parts = line.split()
    if len(parts) < 4 or parts[2] not in LEVELS:
        raise ParseError(line.strip())
    fields = dict(w.split("=", 1) for w in parts[3:] if "=" in w)
    return {"level": parts[2], "time": parts[1], "fields": fields}


def analyse_file(path):
    """Count levels, collect timings and bad lines for one file."""
    stats = {"file": os.path.basename(path), "INFO": 0, "WARNING": 0, "ERROR": 0,
             "bad_lines": 0, "slow": []}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                entry = parse_line(line)
            except ParseError:
                stats["bad_lines"] += 1
                continue
            stats[entry["level"]] += 1
            ms = int(entry["fields"].get("ms", 0))
            if ms >= 1000:
                stats["slow"].append({"time": entry["time"], "ms": ms,
                                      "path": entry["fields"].get("path", "-")})
    return stats


def write_reports(results, json_path, csv_path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["file", *LEVELS, "bad_lines"])
        for r in results:
            writer.writerow([r["file"], *(r[level] for level in LEVELS), r["bad_lines"]])


def main(folder="logs"):
    files = find_log_files(folder)
    print(f"Found {len(files)} log files in '{folder}'")
    results = [analyse_file(path) for path in files]
    write_reports(results, "report.json", "report.csv")

    totals = {level: sum(r[level] for r in results) for level in LEVELS}
    print(f"{'FILE':<12}{'INFO':>6}{'WARN':>6}{'ERROR':>7}{'BAD':>5}")
    for r in results:
        print(f"{r['file']:<12}{r['INFO']:>6}{r['WARNING']:>6}{r['ERROR']:>7}{r['bad_lines']:>5}")
    print(f"{'TOTAL':<12}{totals['INFO']:>6}{totals['WARNING']:>6}{totals['ERROR']:>7}")
    slow = [s | {"file": r["file"]} for r in results for s in r["slow"]]
    for s in sorted(slow, key=lambda s: s["ms"], reverse=True):
        print(f"SLOW: {s['file']} {s['time']} {s['path']} {s['ms']} ms")
    with open("report.csv", encoding="utf-8") as f:
        print("report.csv ->", f.read().splitlines())


main()
