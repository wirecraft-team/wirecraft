import random


def id_to_mac(id: int) -> str:
    """
    Convert an integer ID to a MAC address string.
    To 3 first bytes are random, the last 3 bytes are derived from the ID.

    Example with 7983034:
        In binary, 7983034 is represented as: 0b01111001 11001111 10111010
        We just take the last 3 bytes and convert them to hex:
        01111001 11001111 10111010 -> 79:cf:ba

        The first 3 bytes are random but with set seed to ensure idempotency.
    """
    rand = random.Random(id)  # noqa: S311
    mac = [
        rand.randint(0, 255),
        rand.randint(0, 255),
        rand.randint(0, 255),
        id >> 16,
        (id >> 8) & 0xFF,
        id & 0xFF,
    ]
    return ":".join(f"{byte:02x}" for byte in mac)


def mac_to_id(mac: str) -> int:
    """Revert id_to_mac"""
    parts = mac.split(":")
    if len(parts) != 6:
        raise ValueError(f"Invalid MAC address format: {mac}")
    return int(parts[3], 16) << 16 | int(parts[4], 16) << 8 | int(parts[5], 16)
