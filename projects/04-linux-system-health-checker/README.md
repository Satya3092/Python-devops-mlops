# Project 4 — Linux System Health Checker

**Phase:** after Day 62 (and Day 75) · **Difficulty:** 🟠 Intermediate+ · **Concepts:** `os`, `subprocess`, `logging`, file handling

A dependency-free health checker for Linux servers. It collects **CPU**, **RAM**, **disk usage** and **hostname** using only the standard library (reading `/proc` and calling Linux commands with `subprocess`), evaluates thresholds, logs everything and writes a report.

> Day 75's `server_monitor.py` uses `psutil` (cross-platform). This project deliberately uses **no third-party packages**, so it runs on any minimal Linux box or container — great practice with `os`, `subprocess` and `/proc`.

## What it collects
| Metric | Source |
|---|---|
| Hostname | `socket.gethostname()` / `hostname` command |
| CPU usage % | two samples of `/proc/stat` |
| Load average | `os.getloadavg()` |
| Memory % | `/proc/meminfo` (`MemTotal`, `MemAvailable`) |
| Disk usage % per mount | `df -P` via `subprocess` |
| Uptime | `/proc/uptime` |
| Top processes by memory | `ps -eo pid,comm,%mem --sort=-%mem` |
| Failed systemd units (optional) | `systemctl --failed` |

## Usage
```bash
python3 health_checker.py                              # print report, write logs/ and reports/
python3 health_checker.py --cpu-warn 70 --disk-warn 75
python3 health_checker.py --quiet ; echo "exit code $?"   # for cron/monitoring
```

Exit codes: `0` OK, `1` WARNING, `2` CRITICAL (Nagios style).

Sample output:
```text
========== Linux Health Report ==========
Host      : web-01            Uptime: 12d 03h
CPU       :   7.8%  OK        Load: 0.42 0.38 0.35 (4 cores)
Memory    :  41.2%  OK        (6.4 / 15.5 GiB used)
Disk /    :  83.0%  WARNING
Disk /data:  52.1%  OK
Top memory: java(12.6%) dockerd(3.1%) containerd(1.8%)
Systemd   : 0 failed units
-----------------------------------------
OVERALL   : WARNING
Report saved to reports/health-web-01-20261120-101502.txt
```

## Schedule it
```bash
# crontab -e   (every 10 minutes, keep logs)
*/10 * * * * /usr/bin/python3 /opt/health/health_checker.py --quiet >> /var/log/health-cron.log 2>&1
```
Or create a systemd service + timer (see the comments at the top of the script).

## Files produced
- `logs/health_checker.log` — rotating log (5 × 1 MB)
- `reports/health-<host>-<timestamp>.txt` and `.json`
