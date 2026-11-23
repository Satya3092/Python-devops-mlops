# Day 068 — Command-Line Arguments using argparse

[⬅ Day 067](../../07-devops-automation/day-067/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 069 ➡](../../07-devops-automation/day-069/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 7 — Python for DevOps Automation | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Build professional command-line interfaces with `argparse`
- Use positional arguments, options, flags, types, choices and defaults
- Create sub-commands like `git commit` / `kubectl get`

## 2. Topic Explanation

Automation scripts are run by people, cron and CI — not by someone typing into `input()`. They take **command-line arguments**:

```bash
python backup.py /var/lib/postgres --retention 7 --compress --env prod
```

`sys.argv` gives the raw list of words, but `argparse` (standard library) does the hard work:
- **Positional arguments** (`source`) — required, identified by position.
- **Optional arguments** (`--retention 7`, short form `-r 7`) — with defaults.
- **Flags** (`--compress`) — `action="store_true"` makes them booleans.
- `type=int`, `choices=["dev", "prod"]`, `required=True`, `nargs="+"` (one or more values).
- Automatic `--help` and error messages.
- **Sub-commands** with `add_subparsers()` — like `docker run` / `docker ps`.

`parser.parse_args()` reads `sys.argv`. For testing (and in these examples) you can pass a list: `parser.parse_args(["--env", "prod"])`.

Exit codes matter: `parser.error()` exits with code 2; your script should `sys.exit(0)` on success and non-zero on failure so CI can react.

## 3. Syntax

```python
import argparse
parser = argparse.ArgumentParser(description="What the tool does")
parser.add_argument("source")                                  # positional
parser.add_argument("-r", "--retention", type=int, default=7)  # option
parser.add_argument("--env", choices=["dev", "prod"], required=True)
parser.add_argument("--dry-run", action="store_true")          # flag
args = parser.parse_args()          # args.source, args.retention, args.dry_run
```

| Part | Meaning |
|---|---|
| `add_argument("name")` | Positional (required) argument. |
| `"-x", "--long"` | Optional argument with short and long names; `--dry-run` becomes `args.dry_run`. |
| `type / default / choices` | Conversion, default value and allowed values. |
| `action="store_true"` | Boolean flag. |
| `nargs="+"` | Accept one or more values as a list. |

## 4. Example 1 — Basic Example: A basic CLI parser

```python
import argparse

parser = argparse.ArgumentParser(prog="backup.py", description="Back up a directory.")
parser.add_argument("source", help="directory to back up")
parser.add_argument("-d", "--destination", default="/backups", help="where to store backups")
parser.add_argument("-r", "--retention", type=int, default=7, help="days to keep backups")
parser.add_argument("--env", choices=["dev", "staging", "prod"], default="dev")
parser.add_argument("--compress", action="store_true", help="create .tar.gz")
parser.add_argument("--exclude", nargs="+", default=[], help="patterns to skip")

# In a real script: args = parser.parse_args()  (reads the command line)
args = parser.parse_args(["/var/lib/app", "-r", "14", "--compress", "--env", "prod",
                          "--exclude", "*.tmp", "cache/"])
print(args)
print(f"Backing up {args.source} -> {args.destination} (keep {args.retention} days)")
print("Compress:", args.compress, "| Env:", args.env, "| Exclude:", args.exclude)

defaults = parser.parse_args(["/etc"])
print("With defaults:", vars(defaults))

print()
parser.print_help()
```

## 5. Example 2 — Practical Example: Sub-commands: a tiny 'deployctl' tool

```python
import argparse


def cmd_deploy(args):
    mode = "DRY RUN: would deploy" if args.dry_run else "Deploying"
    return f"{mode} {args.service}:{args.version} to {args.env} with {args.replicas} replicas"


def cmd_rollback(args):
    return f"Rolling back {args.service} in {args.env} by {args.steps} release(s)"


def cmd_status(args):
    services = args.services or ["all services"]
    return f"Status of {', '.join(services)} in {args.env}"


def build_parser():
    parser = argparse.ArgumentParser(prog="deployctl", description="Deployment helper")
    parser.add_argument("--env", choices=["dev", "staging", "prod"], default="dev")
    sub = parser.add_subparsers(dest="command", required=True)

    deploy = sub.add_parser("deploy", help="deploy a version")
    deploy.add_argument("service")
    deploy.add_argument("version")
    deploy.add_argument("--replicas", type=int, default=2)
    deploy.add_argument("--dry-run", action="store_true")
    deploy.set_defaults(func=cmd_deploy)

    rollback = sub.add_parser("rollback", help="roll back a service")
    rollback.add_argument("service")
    rollback.add_argument("--steps", type=int, default=1)
    rollback.set_defaults(func=cmd_rollback)

    status = sub.add_parser("status", help="show status")
    status.add_argument("services", nargs="*")
    status.set_defaults(func=cmd_status)
    return parser


parser = build_parser()
command_lines = [
    ["--env", "prod", "deploy", "orders", "2.5.0", "--replicas", "4"],
    ["deploy", "search", "1.1.0", "--dry-run"],
    ["--env", "staging", "rollback", "payments", "--steps", "2"],
    ["status", "orders", "search"],
]
for argv in command_lines:
    args = parser.parse_args(argv)
    print("$ deployctl", " ".join(argv))
    print("  ", args.func(args))

try:
    parser.parse_args(["deploy", "orders"])          # missing version
except SystemExit as exit_signal:
    print("argparse exited with code", exit_signal.code)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `source` is positional; the others are options with defaults.
- `type=int` converts `"14"` to `14`; `choices` rejects invalid environments.
- `--compress` is a flag (True when present); `--exclude` with `nargs="+"` collects a list.
- `vars(args)` turns the result into a dict. `print_help()` shows the auto-generated help text (`python backup.py --help`).

**Example 2**
- `add_subparsers` creates `deploy`, `rollback` and `status` sub-commands, each with its own arguments.
- `set_defaults(func=...)` attaches a handler function to each sub-command — then `args.func(args)` dispatches (the Day 45 dispatch idea again).
- A missing argument makes argparse print a usage error to stderr and exit with code 2 (we catch `SystemExit` to show it).

## 7. Expected Output

**Example 1:**

```text
Namespace(source='/var/lib/app', destination='/backups', retention=14, env='prod', compress=True, exclude=['*.tmp', 'cache/'])
Backing up /var/lib/app -> /backups (keep 14 days)
Compress: True | Env: prod | Exclude: ['*.tmp', 'cache/']
With defaults: {'source': '/etc', 'destination': '/backups', 'retention': 7, 'env': 'dev', 'compress': False, 'exclude': []}

usage: backup.py [-h] [-d DESTINATION] [-r RETENTION]
                 [--env {dev,staging,prod}] [--compress]
                 [--exclude EXCLUDE [EXCLUDE ...]]
                 source

Back up a directory.

positional arguments:
  source                directory to back up

options:
  -h, --help            show this help message and exit
  -d, --destination DESTINATION
                        where to store backups
  -r, --retention RETENTION
                        days to keep backups
  --env {dev,staging,prod}
  --compress            create .tar.gz
  --exclude EXCLUDE [EXCLUDE ...]
                        patterns to skip
```

**Example 2:**

```text
$ deployctl --env prod deploy orders 2.5.0 --replicas 4
   Deploying orders:2.5.0 to prod with 4 replicas
$ deployctl deploy search 1.1.0 --dry-run
   DRY RUN: would deploy search:1.1.0 to dev with 2 replicas
$ deployctl --env staging rollback payments --steps 2
   Rolling back payments in staging by 2 release(s)
$ deployctl status orders search
   Status of orders, search in dev
argparse exited with code 2
```

## 8. Common Mistakes

**1. Using `input()` in automation**

Cron/CI can't type answers. Use arguments, env vars or config files.

**2. Forgetting `type=int`**

Without it, `args.retention` is the string `"14"` and maths fails.

**3. `--dry-run` attribute name**

Dashes become underscores: access it as `args.dry_run`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Greeter CLI:** Create a parser with a positional `name` and an optional `--times` (int, default 1). Parse `["Asha", "--times", "3"]` and print the greeting that many times.
- **Task 2 (Medium) — Port scanner arguments:** Create a parser for `scan.py` with positional `host`, `--ports` (one or more ints, default `[22, 80, 443]`), `--timeout` (float, default 1.0) and `-v/--verbose` flag. Parse two different command lines and print the resulting namespaces as dicts.
- **Task 3 (Practical Challenge) — log-tool with sub-commands:** Build `logtool` with sub-commands `count` (positional file, `--level` choice INFO/WARNING/ERROR), `tail` (file, `-n` int default 5) and `search` (file, pattern, `--ignore-case` flag). Each handler should actually operate on `../../datasets/app.log`. Run all three sub-commands.

## 10. DevOps/MLOps Connection

- **DevOps:** every internal tool (`deployctl`, `backup.py`, `rotate-keys`) needs a clean CLI so it can be called from cron, Jenkins, GitHub Actions or Ansible.
- **Cloud:** the AWS CLI is an argparse-style Python program with sub-commands (`aws s3 ls`).
- **MLOps:** training scripts take `--data`, `--epochs`, `--learning-rate`, `--output-model` so pipelines (and hyper-parameter searches) can call them with different values.

## 11. Interview Questions

**Q1. What is the difference between `sys.argv` and `argparse`?**

<details><summary>Show answer</summary>

`sys.argv` is the raw list of strings; argparse parses it into typed attributes with validation, defaults, help and errors.

</details>

**Q2. How do you define a boolean flag?**

<details><summary>Show answer</summary>

`parser.add_argument("--verbose", action="store_true")`.

</details>

**Q3. How would you implement `tool start|stop|status` sub-commands?**

<details><summary>Show answer</summary>

`parser.add_subparsers()` with one sub-parser per command and `set_defaults(func=handler)` to dispatch.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 68 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 067](../../07-devops-automation/day-067/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 069 ➡](../../07-devops-automation/day-069/README.md)
