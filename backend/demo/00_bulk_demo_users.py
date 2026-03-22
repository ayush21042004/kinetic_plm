"""
Bulk demo users.

This file is intentionally prefixed with ``00_`` so it executes first inside
``backend/demo`` because the data loader sorts files lexically.
"""

from itertools import cycle


ROLE_CONFIGS = {
    "engineering": {
        "count": 120,
        "role_id": "@role_engineering",
        "password": "$P$engdemo123",
        "email_prefix": "eng",
    },
    "approver": {
        "count": 90,
        "role_id": "@role_approver",
        "password": "$P$approverdemo123",
        "email_prefix": "apr",
    },
    "operations": {
        "count": 90,
        "role_id": "@role_operations",
        "password": "$P$opsdemo123",
        "email_prefix": "ops",
    },
}

TIMEZONE_IDS = [
    "@tz_utc",
    "@tz_americanewyork",
    "@tz_americalosangeles",
    "@tz_europelondon",
    "@tz_asiakolkata",
    "@tz_asiatokyo",
    "@tz_asiasingapore",
]

FIRST_NAMES = [
    "Aarav", "Abigail", "Adrian", "Aisha", "Akash", "Amelia", "Anaya", "Arjun",
    "Aria", "Benjamin", "Camila", "Charlotte", "Daniel", "Diya", "Ethan", "Eva",
    "Fatima", "Grace", "Harper", "Ishaan", "Isla", "Jack", "James", "Kavya",
    "Leo", "Liam", "Lina", "Lucas", "Maya", "Mia", "Mila", "Nathan", "Noah",
    "Nora", "Olivia", "Owen", "Priya", "Riya", "Ryan", "Saanvi", "Samuel",
    "Sara", "Sophia", "Vihaan", "William", "Yash", "Zara",
]

LAST_NAMES = [
    "Adams", "Allen", "Anderson", "Baker", "Brown", "Carter", "Clark", "Collins",
    "Cooper", "Davis", "Diaz", "Edwards", "Evans", "Foster", "Garcia", "Gonzalez",
    "Green", "Hall", "Harris", "Hernandez", "Hill", "Howard", "Jackson", "Johnson",
    "Kelly", "King", "Lee", "Lewis", "Lopez", "Martin", "Martinez", "Miller",
    "Mitchell", "Moore", "Morgan", "Nelson", "Parker", "Patel", "Perez", "Perry",
    "Reed", "Richardson", "Rivera", "Roberts", "Scott", "Taylor", "Thomas", "Turner",
    "Walker", "Ward", "Watson", "White", "Williams", "Wilson", "Wright", "Young",
]


def _build_full_name(index: int) -> str:
    first_name = FIRST_NAMES[index % len(FIRST_NAMES)]
    last_name = LAST_NAMES[(index * 3) % len(LAST_NAMES)]
    return f"{first_name} {last_name}"


def _build_role_records(role_name: str, start_index: int, count: int, config: dict) -> dict:
    records = {}
    timezone_cycle = cycle(TIMEZONE_IDS)

    for offset in range(count):
        user_number = start_index + offset
        xml_id = f"demo_user_{role_name}_{user_number:03d}"
        email = f"{config['email_prefix']}.{user_number:03d}@demo.kinetic.com"

        records[xml_id] = {
            "model": "user",
            "values": {
                "email": email,
                "full_name": _build_full_name(user_number),
                "hashed_password": config["password"],
                "role_id": config["role_id"],
                "timezone_id": next(timezone_cycle),
                "is_active": user_number % 17 != 0,
                "theme": "light" if user_number % 4 == 0 else "dark",
                "show_notification_toasts": user_number % 5 != 0,
            },
        }

    return records


def _build_records() -> dict:
    records = {}
    next_index = 1

    for role_name, config in ROLE_CONFIGS.items():
        count = config["count"]
        records.update(_build_role_records(role_name, next_index, count, config))
        next_index += count

    return records


RECORDS = _build_records()
