"""Network helpers."""


def is_valid_ip(address):
    """Return True if address looks like a valid IPv4 address."""
    parts = address.split(".")
    if len(parts) != 4:
        return False
    return all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)
