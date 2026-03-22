"""
Bulk demo work centers.

Loads after users and product versions, before BOM data.
"""

AREA_DEFINITIONS = [
    ("Fastener Prep", "Bench"),
    ("Machining", "Cell"),
    ("Fabrication", "Bay"),
    ("Frame Assembly", "Line"),
    ("Electrical Panel", "Station"),
    ("Cable Harness", "Cell"),
    ("Sensor Integration", "Bench"),
    ("Drive Assembly", "Line"),
    ("Motion Calibration", "Station"),
    ("Inspection", "Desk"),
]

SHIFT_NAMES = [
    "North", "South", "East", "West", "Central",
    "Alpha", "Bravo", "Charlie", "Delta", "Echo",
]


def _build_records() -> dict:
    records = {}

    for index in range(1, 201):
        area_name, area_type = AREA_DEFINITIONS[(index - 1) % len(AREA_DEFINITIONS)]
        shift_name = SHIFT_NAMES[((index - 1) // len(AREA_DEFINITIONS)) % len(SHIFT_NAMES)]
        zone_number = ((index - 1) // 50) + 1

        xml_id = f"demo_work_center_bulk_{index:03d}"
        name = f"{area_name} {area_type} {shift_name}-{zone_number:02d}"

        records[xml_id] = {
            "model": "work.center",
            "values": {
                "name": name,
            },
        }

    return records


RECORDS = _build_records()
