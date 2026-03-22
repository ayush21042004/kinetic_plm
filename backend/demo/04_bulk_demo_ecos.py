"""
Bulk demo ECOs.

Creates 360 ECOs total:
- 160 product ECOs
- 200 BoM ECOs

Some ECOs are moved through workflow methods so seeded data reflects actual
process transitions, not just static stage assignments.
"""

PRODUCT_TARGETS = [
    {
        "product_xml_id": "@demo_product_controller",
        "label": "Main Controller Board",
        "code_prefix": "MCB",
        "base_sale_price": 12000,
        "base_cost_price": 8500,
    },
    {
        "product_xml_id": "@demo_product_motor",
        "label": "Servo Motor 24V",
        "code_prefix": "SM24",
        "base_sale_price": 4500,
        "base_cost_price": 3000,
    },
    {
        "product_xml_id": "@demo_product_frame",
        "label": "Aluminium Frame Assembly",
        "code_prefix": "AFA",
        "base_sale_price": 7000,
        "base_cost_price": 5200,
    },
    {
        "product_xml_id": "@demo_product_sensor",
        "label": "Position Sensor Module",
        "code_prefix": "PSM",
        "base_sale_price": 1800,
        "base_cost_price": 1100,
    },
    {
        "product_xml_id": "@demo_product_driver",
        "label": "Motor Driver Board",
        "code_prefix": "MDB",
        "base_sale_price": 2200,
        "base_cost_price": 1500,
    },
    {
        "product_xml_id": "@demo_product_cable",
        "label": "Wiring Harness 24V",
        "code_prefix": "WH24",
        "base_sale_price": 950,
        "base_cost_price": 600,
    },
    {
        "product_xml_id": "@demo_product_arm",
        "label": "Robotic Arm Unit",
        "code_prefix": "RAU",
        "base_sale_price": 85000,
        "base_cost_price": 58000,
    },
    {
        "product_xml_id": "@demo_product_gripper",
        "label": "Adaptive Gripper Head",
        "code_prefix": "AGH",
        "base_sale_price": 18500,
        "base_cost_price": 12600,
    },
    {
        "product_xml_id": "@demo_product_power",
        "label": "Auxiliary Power Module",
        "code_prefix": "APM",
        "base_sale_price": 2400,
        "base_cost_price": 1650,
    },
    {
        "product_xml_id": "@demo_product_vision",
        "label": "Vision Alignment Camera",
        "code_prefix": "VAC",
        "base_sale_price": 3200,
        "base_cost_price": 2100,
    },
]

PRODUCT_CHANGE_THEMES = [
    "connector routing update",
    "cost optimization refresh",
    "serviceability improvement",
    "tolerance correction",
    "safety margin update",
    "packaging simplification",
    "calibration enhancement",
    "thermal management update",
]

BOM_CHANGE_THEMES = [
    "hardware consolidation",
    "routing simplification",
    "assembly balancing",
    "inspection improvement",
    "service-kit alignment",
    "cable retention update",
    "subassembly simplification",
    "tooling reduction",
]

WORKORDER_NAMES = [
    "Incoming Material Prep",
    "Subassembly Build",
    "Mechanical Integration",
    "Harness Installation",
    "Torque & Fit Check",
    "Electrical Validation",
    "Calibration Pass",
    "Final Release Inspection",
]

COMPONENT_NOTES = [
    "Replace with updated standard part.",
    "Increase quantity for reinforcement.",
    "Reduce assembly variation in the station.",
    "Align with preferred supplier stock.",
]

WORKORDER_NOTES = [
    "Cycle time aligned to latest takt estimate.",
    "Shifted to specialized work center for consistency.",
    "Inserted to reduce downstream rework risk.",
]


def _initiator_ref(index: int) -> str:
    engineering_slot = ((index - 1) % 40) + 1
    return f"@demo_user_engineering_{engineering_slot:03d}"


def _workflow_mode(index: int) -> str:
    bucket = index % 8
    if bucket in (1, 2):
        return "approval_process"
    if bucket == 3:
        return "refused_rework"
    if bucket == 4:
        return "done_snapshot"
    return "draft"


def _product_record(index: int) -> dict:
    target = PRODUCT_TARGETS[(index - 1) % len(PRODUCT_TARGETS)]
    theme = PRODUCT_CHANGE_THEMES[(index - 1) % len(PRODUCT_CHANGE_THEMES)]
    workflow_mode = _workflow_mode(index)

    values = {
        "type": "product",
        "product_id": target["product_xml_id"],
        "initiated_by_id": _initiator_ref(index),
        "description": f"Product ECO for {target['label']} covering {theme}.",
        "update_version": False,
        "eco_name": f"{target['label']} Rev {index:03d}",
        "eco_default_code": f"{target['code_prefix']}-{200 + index:03d}",
        "eco_sale_price": target["base_sale_price"] + (index % 9) * 75,
        "eco_cost_price": target["base_cost_price"] + (index % 7) * 45,
        "eco_change_notes": (
            f"Requested change set {index:03d} applies {theme} to improve quality, "
            "fit, and maintainability for recurring production."
        ),
    }

    record = {
        "model": "plm.eco",
        "values": values,
    }

    if workflow_mode == "approval_process":
        record["calls"] = ["action_move_to_next_stage"]
    elif workflow_mode == "refused_rework":
        values["stage_id"] = "@stage_refused"
        record["calls"] = ["action_move_to_draft"]
    elif workflow_mode == "done_snapshot":
        values["stage_id"] = "@stage_done"

    return record


def _bom_component_ref(index: int, line_index: int) -> str:
    component_number = ((index * 9) + (line_index * 17)) % 300 + 1
    return f"@demo_version_{_version_key(component_number)}_{component_number:03d}"


def _version_key(number: int) -> str:
    if 1 <= number <= 12:
        return "fastener_socket_head_cap_screw"
    if 13 <= number <= 24:
        return "fastener_hex_bolt"
    if 25 <= number <= 36:
        return "fastener_nylon_lock_nut"
    if 37 <= number <= 48:
        return "washer_flat_stainless"
    if 49 <= number <= 60:
        return "bearing_deep_groove"
    if 61 <= number <= 72:
        return "shaft_coupling_flexible"
    if 73 <= number <= 84:
        return "aluminum_extrusion"
    if 85 <= number <= 96:
        return "sheet_panel_powder_coated"
    if 97 <= number <= 108:
        return "connector_m12_cable"
    if 109 <= number <= 120:
        return "terminal_block_din"
    if 121 <= number <= 132:
        return "power_supply_din"
    if 133 <= number <= 144:
        return "motor_stepper_nema"
    if 145 <= number <= 156:
        return "sensor_photoelectric"
    if 157 <= number <= 168:
        return "controller_plc_module"
    if 169 <= number <= 180:
        return "linear_guide_rail"
    if 181 <= number <= 192:
        return "linear_guide_block"
    if 193 <= number <= 204:
        return "roller_conveyor"
    if 205 <= number <= 216:
        return "proximity_sensor_inductive"
    if 217 <= number <= 228:
        return "relay_interface_module"
    if 229 <= number <= 240:
        return "network_switch_industrial"
    if 241 <= number <= 252:
        return "hmi_operator_panel"
    if 253 <= number <= 264:
        return "pneumatic_cylinder_compact"
    if 265 <= number <= 276:
        return "solenoid_valve_pneumatic"
    if 277 <= number <= 288:
        return "gearbox_planetary"
    return "furniture_work_table"


def _bom_record(index: int) -> dict:
    workflow_mode = _workflow_mode(index + 160)
    theme = BOM_CHANGE_THEMES[(index - 1) % len(BOM_CHANGE_THEMES)]

    line_creates = []
    for line_index in range(1, 4):
        line_creates.append({
            "component_product_id": _bom_component_ref(index, line_index),
            "quantity": ((index + line_index) % 4) + 1,
            "notes": COMPONENT_NOTES[(line_index - 1) % len(COMPONENT_NOTES)],
        })

    workorder_creates = []
    workorder_count = 2 + (index % 2)
    for workorder_index in range(workorder_count):
        work_center_number = ((index * 5) + workorder_index) % 200 + 1
        workorder_creates.append({
            "operation": WORKORDER_NAMES[(index + workorder_index) % len(WORKORDER_NAMES)],
            "work_center_id": f"@demo_work_center_bulk_{work_center_number:03d}",
            "duration_minutes": 18 + ((index + workorder_index) % 8) * 6,
        })

    values = {
        "type": "bom",
        "bom_id": f"@demo_bom_bulk_{index:03d}",
        "initiated_by_id": _initiator_ref(index + 160),
        "description": f"BoM ECO for bulk assembly {index:03d} focused on {theme}.",
        "update_version": index % 3 != 0,
        "eco_line_ids": {"create": line_creates},
        "eco_workorder_ids": {"create": workorder_creates},
    }

    record = {
        "model": "plm.eco",
        "values": values,
    }

    if workflow_mode == "approval_process":
        record["calls"] = ["action_move_to_next_stage"]
    elif workflow_mode == "refused_rework":
        values["stage_id"] = "@stage_refused"
        record["calls"] = ["action_move_to_draft"]
    elif workflow_mode == "done_snapshot":
        values["stage_id"] = "@stage_done"

    return record


def _build_records() -> dict:
    records = {}

    for index in range(1, 161):
        records[f"demo_eco_product_bulk_{index:03d}"] = _product_record(index)

    for index in range(1, 201):
        records[f"demo_eco_bom_bulk_{index:03d}"] = _bom_record(index)

    return records


RECORDS = _build_records()
