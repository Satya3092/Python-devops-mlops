"""
Day 062 — Logging Module: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import logging
import sys
from pathlib import Path

# ===== Task 1 =====
logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s", stream=sys.stdout)
logging.debug("debug")
logging.info("info")
logging.warning("warning")
logging.error("error")
logging.critical("critical")

# ===== Task 2 =====
deploy_log = logging.getLogger("deploy")
deploy_log.setLevel(logging.INFO)
handler = logging.FileHandler("deploy.log", mode="w")
handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
deploy_log.addHandler(handler)
deploy_log.propagate = False
deploy_log.info("Pulling image orders:2.4.1")
deploy_log.info("Applying manifests")
deploy_log.info("Waiting for rollout")
deploy_log.error("Rollout timed out")
handler.close()
print(Path("deploy.log").read_text().strip())

# ===== Task 3 =====
def process_orders(orders, logger):
    processed = 0
    for order in orders:
        try:
            amount = order["amount"]
        except KeyError:
            logger.exception("Order %s has no amount", order.get("id"))
            continue
        logger.debug("Processing order %s (%.2f)", order["id"], amount)
        if amount > 1000:
            logger.warning("Large order %s: %.2f", order["id"], amount)
        processed += 1
    logger.info("Processed %d of %d orders", processed, len(orders))


log = logging.getLogger("orders")
log.setLevel(logging.DEBUG)
console = logging.StreamHandler(sys.stdout)
console.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
log.addHandler(console)
log.propagate = False
process_orders([{"id": 1, "amount": 250.0}, {"id": 2, "amount": 4999.99}, {"id": 3}], log)
