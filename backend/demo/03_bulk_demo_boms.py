"""
Bulk demo BOMs, component lines, and routing workcenter lines.

This file consumes the first 200 bulk product versions from
``01_bulk_demo_product_versions.py`` and creates one BOM for each.
"""

import importlib.util
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PRODUCT_VERSION_FILE = BASE_DIR / "01_bulk_demo_product_versions.py"


def _load_product_version_records():
    spec = importlib.util.spec_from_file_location("bulk_demo_product_versions", PRODUCT_VERSION_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.RECORDS


PRODUCT_VERSION_RECORDS = _load_product_version_records()
PRODUCT_VERSION_IDS = list(PRODUCT_VERSION_RECORDS.keys())
BOM_TARGET_VERSION_IDS = PRODUCT_VERSION_IDS[:200]
COMPONENT_POOL_IDS = PRODUCT_VERSION_IDS

ASSEMBLY_NOTES = [
    "Primary assembly BOM for standard production release.",
    "Configured for pilot line assembly and repeatable workstation flow.",
    "Balanced component set for frame, controls, and installation hardware.",
    "Prepared for downstream routing, inspection, and final verification.",
]

OPERATIONS = [
    ("Kit Components", 12),
    ("Mechanical Assembly", 38),
    ("Electrical Assembly", 42),
    ("Cable Routing", 24),
    ("Sensor Mounting", 18),
    ("Control Panel Wiring", 31),
    ("Torque Verification", 14),
    ("Functional Test", 28),
    ("Calibration", 22),
    ("Final Inspection", 16),
]

COMPONENT_NOTES = [
    "Primary structural component.",
    "Standard hardware pack for assembly.",
    "Electrical integration component.",
    "Motion or support component.",
    "Final fit and fastening item.",
]


def _component_indices(target_index: int):
    start = (target_index * 7) % len(COMPONENT_POOL_IDS)
    offsets = [11, 23, 37, 51, 67]
    return [COMPONENT_POOL_IDS[(start + offset) % len(COMPONENT_POOL_IDS)] for offset in offsets]


def _work_center_ref(target_index: int, operation_index: int) -> str:
    work_center_number = ((target_index * 3) + operation_index) % 200 + 1
    return f"@demo_work_center_bulk_{work_center_number:03d}"


def _build_records() -> dict:
    records = {}

    for idx, version_xml_id in enumerate(BOM_TARGET_VERSION_IDS, start=1):
        bom_xml_id = f"demo_bom_bulk_{idx:03d}"
        records[bom_xml_id] = {
            "model": "mrp.bom",
            "values": {
                "product_version_id": f"@{version_xml_id}",
                "version": 1,
                "state": "active",
                "notes": ASSEMBLY_NOTES[(idx - 1) % len(ASSEMBLY_NOTES)],
            },
        }

        component_ids = _component_indices(idx - 1)
        for line_idx, component_xml_id in enumerate(component_ids, start=1):
            if component_xml_id == version_xml_id:
                continue

            records[f"demo_bom_line_bulk_{idx:03d}_{line_idx:02d}"] = {
                "model": "mrp.bom.line",
                "values": {
                    "bom_id": f"@{bom_xml_id}",
                    "component_product_id": f"@{component_xml_id}",
                    "quantity": ((idx + line_idx) % 4) + 1,
                    "notes": COMPONENT_NOTES[(line_idx - 1) % len(COMPONENT_NOTES)],
                },
            }

        operation_count = 2 + (idx % 2)
        for operation_idx in range(operation_count):
            operation_name, base_duration = OPERATIONS[(idx + operation_idx) % len(OPERATIONS)]
            records[f"demo_routing_bulk_{idx:03d}_{operation_idx + 1:02d}"] = {
                "model": "mrp.routing.workcenter",
                "values": {
                    "bom_id": f"@{bom_xml_id}",
                    "operation": operation_name,
                    "work_center_id": _work_center_ref(idx, operation_idx),
                    "duration_minutes": base_duration + ((idx + operation_idx) % 7) * 3,
                },
            }

    return records


RECORDS = _build_records()
