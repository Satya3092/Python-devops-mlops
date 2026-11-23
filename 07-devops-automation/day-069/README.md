# Day 069 — System Information and Resource Monitoring

[⬅ Day 068](../../07-devops-automation/day-068/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 070 ➡](../../07-devops-automation/day-070/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 7 — Python for DevOps Automation | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Install and use `psutil` for cross-platform system metrics
- Read CPU, memory, disk, network and process information
- Sample metrics over time and calculate rates

## 2. Topic Explanation

`psutil` (*process and system utilities*) is the go-to library for system monitoring in Python. It works on Linux, Windows and macOS and powers tools like Glances and many monitoring agents.

```bash
pip install psutil
```

| Area | psutil call |
|---|---|
| CPU % | `psutil.cpu_percent(interval=1)` (per core: `percpu=True`) |
| Cores | `psutil.cpu_count(logical=False/True)` |
| Memory | `psutil.virtual_memory()` → `.total`, `.available`, `.percent` |
| Swap | `psutil.swap_memory()` |
| Disk usage | `psutil.disk_usage("/")` |
| Partitions | `psutil.disk_partitions()` |
| Network I/O | `psutil.net_io_counters()` → bytes sent/received |
| Boot time | `psutil.boot_time()` |
| Processes | `psutil.process_iter(["pid", "name", "memory_percent"])` |

Important ideas:
- `cpu_percent(interval=1)` **measures for one second**. `interval=None` compares with the previous call (first call returns 0.0).
- Counters (network bytes, disk I/O) only grow. To get a **rate**, take two samples and divide the difference by the elapsed time.
- Processes can disappear while you iterate — catch `psutil.NoSuchProcess` / `AccessDenied`.

## 3. Syntax

```python
import psutil
psutil.cpu_percent(interval=1)
mem = psutil.virtual_memory(); mem.percent
disk = psutil.disk_usage("/"); disk.percent
net = psutil.net_io_counters(); net.bytes_sent
for p in psutil.process_iter(["pid", "name", "memory_percent"]):
    p.info
```

| Part | Meaning |
|---|---|
| `cpu_percent(interval)` | CPU utilisation measured over `interval` seconds. |
| `virtual_memory()` | Named tuple with total/available/used/percent. |
| `disk_usage(path)` | Usage of the filesystem containing `path`. |
| `net_io_counters()` | Cumulative network counters since boot. |
| `process_iter(attrs)` | Iterate processes, prefetching attributes into `.info`. |

## 4. Example 1 — Basic Example: A snapshot of the machine

```python
import datetime
import psutil

GB = 1024 ** 3

cpu = psutil.cpu_percent(interval=1)
per_core = psutil.cpu_percent(interval=1, percpu=True)
mem = psutil.virtual_memory()
swap = psutil.swap_memory()
disk = psutil.disk_usage("/")
boot = datetime.datetime.fromtimestamp(psutil.boot_time())

print(f"CPU usage      : {cpu}% over {psutil.cpu_count()} logical cores")
print(f"Per core       : {per_core}")
print(f"Memory         : {mem.used / GB:.1f} / {mem.total / GB:.1f} GB ({mem.percent}%)")
print(f"Available mem  : {mem.available / GB:.1f} GB")
print(f"Swap used      : {swap.percent}%")
print(f"Disk /         : {disk.used / GB:.1f} / {disk.total / GB:.1f} GB ({disk.percent}%)")
print(f"Booted at      : {boot:%Y-%m-%d %H:%M}")
print(f"Uptime (hours) : {(datetime.datetime.now() - boot).total_seconds() / 3600:.1f}")
```

## 5. Example 2 — Practical Example: Network throughput and the top processes

```python
import time
import psutil

# Network rate = difference between two samples / elapsed time
before = psutil.net_io_counters()
time.sleep(2)
after = psutil.net_io_counters()
sent_rate = (after.bytes_sent - before.bytes_sent) / 2 / 1024
recv_rate = (after.bytes_recv - before.bytes_recv) / 2 / 1024
print(f"Network: sent {sent_rate:.1f} KB/s, received {recv_rate:.1f} KB/s")

# Top 5 processes by memory
processes = []
for proc in psutil.process_iter(["pid", "name", "username", "memory_percent"]):
    try:
        processes.append(proc.info)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue
top = sorted(processes, key=lambda p: p["memory_percent"] or 0, reverse=True)[:5]
print(f"{'PID':>7}  {'NAME':<18}{'USER':<12}{'MEM%':>6}")
for p in top:
    print(f"{p['pid']:>7}  {(p['name'] or '?')[:17]:<18}{(p['username'] or '?')[:11]:<12}{p['memory_percent'] or 0:>6.1f}")

# Mounted filesystems that are getting full
for part in psutil.disk_partitions(all=False):
    try:
        usage = psutil.disk_usage(part.mountpoint)
    except PermissionError:
        continue
    flag = "  <-- check!" if usage.percent > 80 else ""
    print(f"{part.mountpoint:<12} {part.fstype:<6} {usage.percent:>5.1f}%{flag}")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `cpu_percent(interval=1)` blocks for one second while measuring.
- Memory and disk objects expose `.total`, `.used`, `.percent`. Dividing by `1024 ** 3` converts bytes to GB.
- `boot_time()` returns a Unix timestamp; converting it gives the boot date and uptime.

**Example 2**
- Network counters are cumulative, so we take two samples 2 seconds apart and divide the difference by 2 → bytes per second.
- `process_iter([...])` prefetches attributes into `proc.info`; processes that vanish or are protected raise exceptions we skip.
- `disk_partitions()` lists mounted filesystems; each is checked for high usage (`df -h` in Python).

## 7. Expected Output

**Example 1:**

```text
CPU usage      : 7.5% over 4 logical cores
Per core       : [9.0, 4.0, 8.1, 6.9]
Memory         : 5.2 / 15.5 GB (38.4%)
Available mem  : 9.6 GB
Swap used      : 0.0%
Disk /         : 41.3 / 97.9 GB (44.4%)
Booted at      : 2026-11-08 09:12
Uptime (hours) : 289.4
```

**Example 2:**

```text
Network: sent 3.4 KB/s, received 18.9 KB/s
    PID  NAME              USER          MEM%
   1342  java              jenkins       12.6
   2210  dockerd           root           3.1
    987  containerd        root           1.8
   4521  python3           ubuntu         0.9
    612  systemd-journal   root           0.4
/            ext4    44.4%
/boot/efi    vfat     6.1%
/data        xfs     83.2%  <-- check!
```

> ℹ️ This lesson reads live information from your machine, so your numbers, names and times will differ from the sample output shown. Install psutil first: `pip install psutil`.

## 8. Common Mistakes

**1. `cpu_percent()` returns 0.0**

With `interval=None` the first call has no baseline. Use `interval=1` or call it twice.

**2. Reading counters as rates**

`bytes_sent` is a total since boot, not per second. Sample twice and divide by elapsed time.

**3. Crashing on vanished processes**

Processes come and go. Wrap per-process access in try/except `psutil.NoSuchProcess, psutil.AccessDenied`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — One-line status:** Print one line with CPU %, memory % and root disk % using psutil.
- **Task 2 (Medium) — Sampling loop:** Take 3 samples (1 second apart) of CPU and memory %, print each, then print the average and peak CPU.
- **Task 3 (Practical Challenge) — Process report:** List processes using more than 1 % memory (name, pid, %), sorted descending, print their combined memory share and the total number of processes.

## 10. DevOps/MLOps Connection

- **DevOps:** custom health checks, Nagios/Zabbix plugins, and lightweight agents that push metrics to Prometheus Pushgateway or CloudWatch.
- **Cloud:** right-sizing — collect real utilisation before choosing an instance type; detect idle instances.
- **MLOps:** monitor GPU/CPU/memory during training and inference; a model server running out of memory is a classic production incident.

## 11. Interview Questions

**Q1. Why does `psutil.cpu_percent()` sometimes return 0.0?**

<details><summary>Show answer</summary>

With no interval it compares against the previous call; the first call has no baseline.

</details>

**Q2. How do you compute network throughput from psutil counters?**

<details><summary>Show answer</summary>

Take two `net_io_counters()` samples, subtract, and divide by the elapsed seconds.

</details>

**Q3. What is the difference between `available` and `free` memory on Linux?**

<details><summary>Show answer</summary>

`free` is completely unused RAM; `available` also counts reclaimable cache/buffers and better represents memory usable by new processes.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 69 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 068](../../07-devops-automation/day-068/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 070 ➡](../../07-devops-automation/day-070/README.md)
