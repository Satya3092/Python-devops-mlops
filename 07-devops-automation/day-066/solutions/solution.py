"""
Day 066 — Python System Administration Automation: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import getpass
import os
import platform
import socket
from pathlib import Path

# ===== Task 1 =====
print(f"{getpass.getuser()}@{socket.gethostname()} | {platform.system()} "
      f"{'.'.join(platform.release().split('.')[:2])} | {os.cpu_count()} CPUs | Python {platform.python_version()}")

# ===== Task 2 =====
PASSWD = """root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
sshd:x:110:65534::/run/sshd:/usr/sbin/nologin
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
asha:x:1001:1001:Asha:/home/asha:/bin/zsh
jenkins:x:998:998:Jenkins:/var/lib/jenkins:/bin/bash"""
for line in PASSWD.splitlines():
    user, _, uid, _, _, home, shell = line.split(":")
    uid = int(uid)
    if shell in ("/bin/bash", "/bin/zsh") and (uid >= 1000 or uid == 0):
        print(f"{user:<8} uid={uid:<5} home={home}")

# ===== Task 3 =====
def ensure_host_entry(path, ip, hostname):
    path = Path(path)
    lines = path.read_text().splitlines() if path.exists() else []
    for i, line in enumerate(lines):
        parts = line.split()
        if len(parts) >= 2 and not line.startswith("#") and hostname in parts[1:]:
            if parts[0] == ip:
                return "unchanged"
            lines[i] = f"{ip} {hostname}"
            path.write_text("\n".join(lines) + "\n")
            return "updated"
    lines.append(f"{ip} {hostname}")
    path.write_text("\n".join(lines) + "\n")
    return "added"


hosts = Path("hosts_demo")
hosts.write_text("127.0.0.1 localhost\n")
print(ensure_host_entry(hosts, "10.0.0.20", "db.internal"))
print(ensure_host_entry(hosts, "10.0.0.20", "db.internal"))
print(ensure_host_entry(hosts, "10.0.0.21", "db.internal"))
print(hosts.read_text(), end="")
