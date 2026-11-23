"""
server_monitor.py - Day 75 DevOps Automation Project.

Collects CPU, memory, disk, hostname and IP address, evaluates thresholds,
logs everything, and writes JSON + text reports.

Usage:
    python server_monitor.py                       # one check with defaults
    python server_monitor.py --cpu-warn 70 --disk-warn 80 --output-dir reports
    python server_monitor.py --json                # print JSON to stdout
Exit codes: 0 = OK, 1 = WARNING, 2 = CRITICAL, 3 = monitoring error
"""
import argparse
import json
import logging
import os
import platform
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import psutil
except ImportError:                      # the tool still works (with fewer metrics)
    psutil = None

LOG = logging.getLogger("server_monitor")
STATUS_ORDER = {"OK": 0, "WARNING": 1, "CRITICAL": 2}


def get_hostname():
    return socket.gethostname()


def get_ip_address():
    """Best effort: the IP used for outbound traffic, falling back to the hostname lookup."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("10.255.255.255", 1))   # no packet is actually sent for UDP connect
            return sock.getsockname()[0]
    except OSError:
        try:
            return socket.gethostbyname(socket.gethostname())
        except OSError:
            return "unknown"


def get_cpu_percent(interval=1.0):
    if psutil:
        return psutil.cpu_percent(interval=interval)
    if hasattr(os, "getloadavg"):         # fallback: 1-minute load / cores
        return round(os.getloadavg()[0] / (os.cpu_count() or 1) * 100, 1)
    raise RuntimeError("cannot read CPU usage (install psutil)")


def get_memory():
    if not psutil:
        raise RuntimeError("cannot read memory usage (install psutil)")
    mem = psutil.virtual_memory()
    return {"total_gb": round(mem.total / 1024 ** 3, 2), "used_percent": mem.percent}


def get_disk(path="/"):
    if psutil:
        usage = psutil.disk_usage(path)
    else:
        import shutil
        usage = shutil.disk_usage(path)
    used_percent = round(usage.used / usage.total * 100, 1)
    return {"path": path, "total_gb": round(usage.total / 1024 ** 3, 2),
            "free_gb": round(usage.free / 1024 ** 3, 2), "used_percent": used_percent}


def classify(value, warning, critical):
    if value >= critical:
        return "CRITICAL"
    if value >= warning:
        return "WARNING"
    return "OK"


def collect(args):
    """Collect every metric; a failing metric is recorded, not fatal."""
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "hostname": get_hostname(),
        "ip_address": get_ip_address(),
        "os": f"{platform.system()} {platform.release()}",
        "checks": {},
        "errors": [],
    }
    checks = [
        ("cpu", lambda: get_cpu_percent(args.interval), args.cpu_warn, args.cpu_crit),
        ("memory", lambda: get_memory()["used_percent"], args.mem_warn, args.mem_crit),
        ("disk", lambda: get_disk(args.disk_path)["used_percent"], args.disk_warn, args.disk_crit),
    ]
    for name, reader, warning, critical in checks:
        try:
            value = reader()
        except Exception as error:          # one broken metric must not stop the others
            LOG.error("Could not read %s: %s", name, error)
            report["errors"].append(f"{name}: {error}")
            continue
        status = classify(value, warning, critical)
        report["checks"][name] = {"value": value, "status": status,
                                  "warning": warning, "critical": critical}
        log_level = logging.INFO if status == "OK" else logging.WARNING
        LOG.log(log_level, "%s=%.1f%% status=%s", name, value, status)

    statuses = [c["status"] for c in report["checks"].values()]
    report["overall"] = max(statuses, key=STATUS_ORDER.get) if statuses else "UNKNOWN"
    return report


def to_text(report):
    lines = [
        "=" * 50,
        f"Server Health Report - {report['hostname']} ({report['ip_address']})",
        f"Time: {report['timestamp']}   OS: {report['os']}",
        "=" * 50,
    ]
    for name, check in report["checks"].items():
        lines.append(f"{name.upper():<8}{check['value']:>6.1f}%   {check['status']:<9}"
                     f"(warn {check['warning']}%, crit {check['critical']}%)")
    for error in report["errors"]:
        lines.append(f"ERROR   {error}")
    lines.append("-" * 50)
    lines.append(f"OVERALL: {report['overall']}")
    return "\n".join(lines)


def save_reports(report, output_dir):
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    json_path = folder / f"health-{report['hostname']}-{stamp}.json"
    text_path = json_path.with_suffix(".txt")
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    text_path.write_text(to_text(report) + "\n", encoding="utf-8")
    return json_path, text_path


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Collect server health metrics and write a report.")
    parser.add_argument("--cpu-warn", type=float, default=float(os.getenv("CPU_WARN", 75)))
    parser.add_argument("--cpu-crit", type=float, default=float(os.getenv("CPU_CRIT", 90)))
    parser.add_argument("--mem-warn", type=float, default=80.0)
    parser.add_argument("--mem-crit", type=float, default=90.0)
    parser.add_argument("--disk-warn", type=float, default=80.0)
    parser.add_argument("--disk-crit", type=float, default=90.0)
    parser.add_argument("--disk-path", default="/" if os.name != "nt" else "C:\\")
    parser.add_argument("--interval", type=float, default=1.0, help="CPU sampling seconds")
    parser.add_argument("--output-dir", default="reports")
    parser.add_argument("--log-file", default="server_monitor.log")
    parser.add_argument("--json", action="store_true", help="print JSON instead of text")
    return parser.parse_args(argv)


def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[logging.FileHandler(log_file, encoding="utf-8")],
    )


def main(argv=None):
    args = parse_args(argv)
    setup_logging(args.log_file)
    try:
        report = collect(args)
        json_path, text_path = save_reports(report, args.output_dir)
    except Exception as error:
        LOG.exception("Monitoring run failed")
        print(f"Monitoring failed: {error}", file=sys.stderr)
        return 3
    print(json.dumps(report, indent=2) if args.json else to_text(report))
    print(f"\nReports written: {json_path} and {text_path.name}")
    return STATUS_ORDER.get(report["overall"], 3)


if __name__ == "__main__":
    sys.exit(main())
