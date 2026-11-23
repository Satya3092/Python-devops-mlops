"""
Day 068 — Command-Line Arguments using argparse
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — A basic CLI parser
# ======================================================================
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

# ======================================================================
# Example 2 — Sub-commands: a tiny 'deployctl' tool
# ======================================================================
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
