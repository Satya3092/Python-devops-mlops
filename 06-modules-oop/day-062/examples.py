"""
Day 062 — Logging Module
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Levels and formatting
# ======================================================================
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-8s %(name)s: %(message)s",   # no time so the output is stable
    stream=sys.stdout,
)
log = logging.getLogger("demo")

log.debug("Not shown: DEBUG is below INFO")
log.info("Application started")
log.warning("Disk usage at %d%%", 82)          # lazy % formatting
log.error("Could not connect to %s", "db-01")
log.critical("Out of memory - shutting down")

try:
    1 / 0
except ZeroDivisionError:
    log.exception("Calculation failed")

# ======================================================================
# Example 2 — Console + rotating file logging for a backup job
# ======================================================================
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(name, log_file, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)                       # console: INFO and above
    console.setFormatter(logging.Formatter("%(levelname)s | %(message)s"))

    file_handler = RotatingFileHandler(log_file, maxBytes=2000, backupCount=2)
    file_handler.setLevel(logging.DEBUG)                 # file: everything
    file_handler.setFormatter(logging.Formatter("%(levelname)s %(name)s line %(lineno)d: %(message)s"))

    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger


log = setup_logger("backup", "backup.log")
databases = ["orders", "users", "payments"]
log.info("Backup job started for %d databases", len(databases))
for db in databases:
    log.debug("Connecting to %s", db)
    if db == "payments":
        log.error("Backup of %s failed: permission denied", db)
        continue
    log.info("Backed up %s", db)
log.info("Backup job finished")

print("--- backup.log (file contains DEBUG lines too) ---")
print(Path("backup.log").read_text().strip())
