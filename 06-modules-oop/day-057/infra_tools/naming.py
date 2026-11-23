"""Naming-convention helpers."""


def hostname(service, env, index):
    """Build a hostname such as orders-prod-01."""
    return f"{service}-{env}-{index:02d}"
