#!/usr/bin/env python3
"""
Project 4 - Linux System Health Checker (standard library only).

Collects CPU, RAM, disk and hostname using /proc and subprocess, evaluates
thresholds, logs results and writes text + JSON reports.

Usage:  python3 health_checker.py [--cpu-warn 80] [--cpu-crit 95] [--mem-warn 80] [--mem-crit 95]
                                  [--disk-warn 80] [--disk-crit 90] [--quiet]
systemd timer example:
    /etc/systemd/system/health.service  -> ExecStart=/usr/bin/python3 /opt/health/health_checker.py --quiet
    /etc/systemd/system/health.timer    -> OnCalendar=*:0/10   (then: systemctl enable --now health.timer)
"""
import argparse
import json
import logging
import os
import shutil
import socket
import subprocess
import sys
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOG = logging.getLogger("health_checker")
ORDER = {"OK": 0, "WARNING": 1, "CRITICAL": 2}


def run(command, timeout=10):
    """Run a command safely; return stdout or '' on any failure."""
    if shutil.which(command[0]) is None:
        LOG.debug("command not found: %s", command[0])
        return ""
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        LOG.warning("command timed out: %s", " ".join(command))
        return ""
    if result.returncode != 0:
        LOG.debug("command failed (%s): %s", result.returncode, result.stderr.strip())
    return result.stdout


def read_cpu_times():
    with open("/proc/stat") as f:
        values = [int(v) for v in f.readline().split()[1:]]
    idle = values[3] + values[4]            # idle + iowait
    return idle, sum(values)


def cpu_percent(interval=1.0):
    idle1, total1 = read_cpu_times()
    time.sleep(interval)
    idle2, total2 = read_cpu_times()
    busy = (total2 - total1) - (idle2 - idle1)
    return round(busy / (total2 - total1) * 100, 1) if total2 > total1 else 0.0


def memory_info():
    info = {}
    with open("/proc/meminfo") as f:
        for line in f:
            key, value = line.split(":", 1)
            info[key] = int(value.split()[0])          # kB
    total, available = info["MemTotal"], info.get("MemAvailable", info["MemFree"])
    used = total - available
    return {"percent": round(used / total * 100, 1), "used_gib": round(used / 1024 ** 2, 1),
            "total_gib": round(total / 1024 ** 2, 1)}


def disk_usage():
    """Parse 'df -P' (POSIX format) into {mount: percent}, skipping pseudo filesystems."""
    disks = {}
    for line in run(["df", "-P", "-x", "tmpfs", "-x", "devtmpfs", "-x", "overlay", "-x", "squashfs"]).splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 6 and parts[4].endswith("%"):
            disks[parts[5]] = float(parts[4].rstrip("%"))
    if not disks:                                         # fallback without df
        total, used, _ = shutil.disk_usage("/")
        disks["/"] = round(used / total * 100, 1)
    return disks


def uptime_text():
    with open("/proc/uptime") as f:
        seconds = int(float(f.read().split()[0]))
    days, rest = divmod(seconds, 86400)
    return f"{days}d {rest // 3600:02d}h"


def top_processes(n=3):
    rows = []
    for line in run(["ps", "-eo", "comm,%mem", "--sort=-%mem"]).splitlines()[1:n + 1]:
        name, mem = line.rsplit(None, 1)
        rows.append(f"{name.strip()}({mem}%)")
    return rows


def failed_units():
    output = run(["systemctl", "--failed", "--no-legend", "--plain"])
    return [line.split()[0] for line in output.splitlines() if line.strip()]


def classify(value, warning, critical):
    return "CRITICAL" if value >= critical else "WARNING" if value >= warning else "OK"


def collect(args):
    load = os.getloadavg()
    cores = os.cpu_count() or 1
    cpu = cpu_percent(args.interval)
    mem = memory_info()
    disks = disk_usage()
    checks = {"cpu": classify(cpu, args.cpu_warn, args.cpu_crit),
              "memory": classify(mem["percent"], args.mem_warn, args.mem_crit)}
    for mount, percent in disks.items():
        checks[f"disk {mount}"] = classify(percent, args.disk_warn, args.disk_crit)
    failed = failed_units()
    if failed:
        checks["systemd"] = "WARNING"
    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "hostname": socket.gethostname(),
        "uptime": uptime_text(),
        "cpu_percent": cpu,
        "load_average": [round(x, 2) for x in load],
        "cores": cores,
        "memory": mem,
        "disks": disks,
        "top_processes": top_processes(),
        "failed_units": failed,
        "checks": checks,
        "overall": max(checks.values(), key=ORDER.get),
    }


def format_report(r):
    lines = ["=" * 10 + " Linux Health Report " + "=" * 10,
             f"Host      : {r['hostname']:<18}Uptime: {r['uptime']}",
             f"CPU       : {r['cpu_percent']:>5.1f}%  {r['checks']['cpu']:<9} Load: "
             f"{' '.join(str(x) for x in r['load_average'])} ({r['cores']} cores)",
             f"Memory    : {r['memory']['percent']:>5.1f}%  {r['checks']['memory']:<9} "
             f"({r['memory']['used_gib']} / {r['memory']['total_gib']} GiB used)"]
    for mount, percent in r["disks"].items():
        lines.append(f"Disk {mount:<5}: {percent:>5.1f}%  {r['checks'][f'disk {mount}']}")
    lines.append(f"Top memory: {' '.join(r['top_processes']) or 'n/a'}")
    lines.append(f"Systemd   : {len(r['failed_units'])} failed units {', '.join(r['failed_units'])}".rstrip())
    lines += ["-" * 41, f"OVERALL   : {r['overall']}"]
    return "\n".join(lines)


def save(report, text):
    folder = BASE_DIR / "reports"
    folder.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base = folder / f"health-{report['hostname']}-{stamp}"
    base.with_suffix(".txt").write_text(text + "\n")
    base.with_suffix(".json").write_text(json.dumps(report, indent=2))
    return base.with_suffix(".txt")


def setup_logging(verbose):
    (BASE_DIR / "logs").mkdir(exist_ok=True)
    handler = RotatingFileHandler(BASE_DIR / "logs" / "health_checker.log", maxBytes=1_000_000, backupCount=5)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    LOG.addHandler(handler)
    LOG.setLevel(logging.DEBUG if verbose else logging.INFO)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Linux system health checker")
    for name, warn, crit in (("cpu", 80, 95), ("mem", 80, 95), ("disk", 80, 90)):
        parser.add_argument(f"--{name}-warn", type=float, default=warn)
        parser.add_argument(f"--{name}-crit", type=float, default=crit)
    parser.add_argument("--interval", type=float, default=1.0, help="CPU sampling seconds")
    parser.add_argument("--quiet", action="store_true", help="only print the overall status")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    if sys.platform != "linux":
        print("This checker reads /proc and only runs on Linux (use Day 75's psutil version elsewhere).")
        return 3
    setup_logging(args.verbose)
    try:
        report = collect(args)
    except (OSError, ValueError) as error:
        LOG.exception("health check failed")
        print(f"UNKNOWN - health check failed: {error}")
        return 3
    text = format_report(report)
    path = save(report, text)
    LOG.info("overall=%s cpu=%s mem=%s disks=%s", report["overall"], report["cpu_percent"],
             report["memory"]["percent"], report["disks"])
    if args.quiet:
        problems = [f"{k}={v}" for k, v in report["checks"].items() if v != "OK"]
        print(f"{report['overall']} - {report['hostname']} " + (", ".join(problems) or "all checks OK"))
    else:
        print(text)
        print(f"Report saved to {path.relative_to(BASE_DIR)}")
    return ORDER[report["overall"]]


if __name__ == "__main__":
    sys.exit(main())
