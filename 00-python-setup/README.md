# 00 — Python Setup Guide

[🏠 Home](../README.md) | [Day 001 ➡](../01-python-fundamentals/day-001/README.md)

Do this once before Day 1. It takes about 20–30 minutes.

## 1. Install Python 3.12 (3.10+ works)

### Windows 10/11
1. Go to <https://www.python.org/downloads/windows/> and download the latest **Python 3.12 Windows installer (64-bit)**.
2. Run it. On the first screen **tick ✅ "Add python.exe to PATH"** (very important), then click **Install Now**.
3. At the end click **"Disable path length limit"** if offered.
4. Open **PowerShell** (Start → type *PowerShell*) and run:
   ```powershell
   python --version        # Python 3.12.x
   pip --version
   ```
5. If `python` opens the Microsoft Store instead: *Settings → Apps → Advanced app settings → App execution aliases* → turn off the two *python* aliases, then reopen PowerShell.

Alternative: `winget install Python.Python.3.12`.

> 💡 DevOps tip: install **WSL2 + Ubuntu** (`wsl --install`) and follow the Linux steps — most DevOps tooling feels native there.

### Ubuntu / Debian
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
python3 --version
```
Ubuntu 24.04 ships Python 3.12. On older releases you can use the deadsnakes PPA (`sudo add-apt-repository ppa:deadsnakes/ppa`) or `pyenv`.

### RHEL / Rocky / Amazon Linux
```bash
sudo dnf install -y python3.12 python3.12-pip
python3.12 --version
```

### macOS
`brew install python@3.12` (with Homebrew) or the installer from python.org.

## 2. Windows vs Linux command names

| Task | Windows | Linux/macOS |
|---|---|---|
| Run Python | `python` / `py` | `python3` |
| pip | `pip` / `py -m pip` | `pip3` / `python3 -m pip` |
| Activate venv | `.venv\Scripts\activate` | `source .venv/bin/activate` |

In the lessons we write `python`; use `python3` on Linux/macOS if `python` is not found.

## 3. Install VS Code
1. Download from <https://code.visualstudio.com/> (or `sudo snap install code --classic` on Ubuntu).
2. Extensions (Ctrl+Shift+X): **Python**, **Pylance**; optional **Ruff**, **Jupyter**, **Docker**, **YAML**, **GitLens**.
3. Recommended settings (*File → Preferences → Settings*, search and set):
   - *Editor: Format On Save* ✅
   - *Editor: Insert Spaces* ✅ and *Tab Size* `4`
   - *Files: Trim Trailing Whitespace* ✅
4. Open the repository folder (*File → Open Folder*), then `Ctrl+Shift+P` → **Python: Select Interpreter** → pick `.venv`.

## 4. Clone the repo and create a virtual environment
```bash
git clone https://github.com/<your-github-username>/100-days-python-devops-mlops.git
cd 100-days-python-devops-mlops
python3 -m venv .venv
source .venv/bin/activate              # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
```
You know isolation from containers — a virtual environment is the Python equivalent: each project gets its own packages.

## 5. Your first run
```bash
python 00-python-setup/verify_setup.py
cd 01-python-fundamentals/day-001
python examples.py
```

## 6. The REPL (interactive shell)
Type `python` (or `python3`) without a file name:
```text
>>> 2 + 3
5
>>> print("Hello")
Hello
>>> exit()
```

## 7. Optional tools for later phases
| Tool | Needed for | Install |
|---|---|---|
| Docker | Days 99–100, Project 8 | <https://docs.docker.com/get-docker/> |
| AWS CLI v2 + account | Day 82, Project 5 | <https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html> |
| kubectl + kind/minikube | Project 8 (optional) | <https://kind.sigs.k8s.io/> |

## Troubleshooting
| Problem | Fix |
|---|---|
| `python: command not found` | use `python3`, or reinstall with *Add to PATH* ticked |
| `pip: externally-managed-environment` (Ubuntu 23.04+) | you're outside a venv — activate `.venv` first |
| PowerShell blocks `activate` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `ModuleNotFoundError: No module named 'pandas'` | activate the venv and install that phase's requirements |
| VS Code uses the wrong Python | *Python: Select Interpreter* → `.venv` |
