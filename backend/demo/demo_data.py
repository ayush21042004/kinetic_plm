RECORDS = {
    # ── Demo: Engineering User ─────────────────────────────────────────────────
    "demo_user_engineering": {
        "model": "user",
        "values": {
            "email": "engineer@kinetic.com",
            "full_name": "Alex Chen",
            "hashed_password": "$P$engineer123",
            "role_id": "@role_engineering",
            "timezone_id": "@tz_utc",
            "is_active": True
        }
    },

    # ── Demo: Approver User ────────────────────────────────────────────────────
    "demo_user_approver": {
        "model": "user",
        "values": {
            "email": "approver@kinetic.com",
            "full_name": "Sarah Mitchell",
            "hashed_password": "$P$approver123",
            "role_id": "@role_approver",
            "timezone_id": "@tz_utc",
            "is_active": True
        }
    },

    # ── Demo: Operations User ──────────────────────────────────────────────────
    "demo_user_operations": {
        "model": "user",
        "values": {
            "email": "ops@kinetic.com",
            "full_name": "Marcus Webb",
            "hashed_password": "$P$ops123",
            "role_id": "@role_operations",
            "timezone_id": "@tz_utc",
            "is_active": True
        }
    },

    # ── Demo: Approval Rule For ECO Approval Stage ────────────────────────────
    "demo_stage_approval_rule_approver": {
        "model": "plm.eco.stage.line",
        "values": {
            "stage_id": "@stage_approval",
            "user_id": "@demo_user_approver",
            "approval_required": True,
        }
    },

    # ── Demo: Products ─────────────────────────────────────────────────────────
    "demo_product_controller": {
        "model": "product.product",
        "values": {
            "name": "Main Controller Board",
            "active": True,
        }
    },
    "demo_product_motor": {
        "model": "product.product",
        "values": {
            "name": "Servo Motor 24V",
            "active": True,
        }
    },
    "demo_product_frame": {
        "model": "product.product",
        "values": {
            "name": "Aluminium Frame Assembly",
            "active": True,
        }
    },

    # ── Demo: Product Versions (v1) ────────────────────────────────────────────
    # The Version.create override will auto-set current_version_id on the product.
    "demo_version_controller_v1": {
        "model": "product.version",
        "values": {
            "product_id": "@demo_product_controller",
            "version": 1,
            "name": "Main Controller Board",
            "default_code": "MCB-001",
            "description": "Initial release of the main controller board.",
            "state": "active",
            "sale_price": 12000,
            "cost_price": 8500,
        }
    },
    "demo_version_motor_v1": {
        "model": "product.version",
        "values": {
            "product_id": "@demo_product_motor",
            "version": 1,
            "name": "Servo Motor 24V",
            "default_code": "SM24-001",
            "description": "Initial release of the 24V servo motor.",
            "state": "active",
            "sale_price": 4500,
            "cost_price": 3000,
        }
    },
    "demo_version_frame_v1": {
        "model": "product.version",
        "values": {
            "product_id": "@demo_product_frame",
            "version": 1,
            "name": "Aluminium Frame Assembly",
            "default_code": "AFA-001",
            "description": "Initial release of the aluminium frame assembly.",
            "state": "active",
            "sale_price": 7000,
            "cost_price": 5200,
        }
    },

    # ── Demo: Additional Component Products ────────────────────────────────────
    "demo_product_sensor": {
        "model": "product.product",
        "values": {
            "name": "Position Sensor Module",
            "active": True,
        }
    },
    "demo_product_driver": {
        "model": "product.product",
        "values": {
            "name": "Motor Driver Board",
            "active": True,
        }
    },
    "demo_product_cable": {
        "model": "product.product",
        "values": {
            "name": "Wiring Harness 24V",
            "active": True,
        }
    },
    "demo_product_arm": {
        "model": "product.product",
        "values": {
            "name": "Robotic Arm Unit",
            "active": True,
        }
    },

    # ── Demo: Versions for new component products ──────────────────────────────
    "demo_version_sensor_v1": {
        "model": "product.version",
        "values": {
            "product_id": "@demo_product_sensor",
            "version": 1,
            "name": "Position Sensor Module",
            "default_code": "PSM-001",
            "description": "Magnetic rotary position sensor, 12-bit resolution.",
            "state": "active",
            "sale_price": 1800,
            "cost_price": 1100,
        }
    },
    "demo_version_driver_v1": {
        "model": "product.version",
        "values": {
            "product_id": "@demo_product_driver",
            "version": 1,
            "name": "Motor Driver Board",
            "default_code": "MDB-001",
            "description": "Dual H-bridge motor driver, 24V/10A.",
            "state": "active",
            "sale_price": 2200,
            "cost_price": 1500,
        }
    },
    "demo_version_cable_v1": {
        "model": "product.version",
        "values": {
            "product_id": "@demo_product_cable",
            "version": 1,
            "name": "Wiring Harness 24V",
            "default_code": "WH24-001",
            "description": "Pre-crimped wiring harness for 24V servo systems.",
            "state": "active",
            "sale_price": 950,
            "cost_price": 600,
        }
    },
    "demo_version_arm_v1": {
        "model": "product.version",
        "values": {
            "product_id": "@demo_product_arm",
            "version": 1,
            "name": "Robotic Arm Unit",
            "default_code": "RAU-001",
            "description": "6-axis robotic arm unit, initial release.",
            "state": "active",
            "sale_price": 85000,
            "cost_price": 58000,
        }
    },
    "demo_product_gripper": {
        "model": "product.product",
        "values": {
            "name": "Adaptive Gripper Head",
            "active": True,
        }
    },
    "demo_product_power": {
        "model": "product.product",
        "values": {
            "name": "Auxiliary Power Module",
            "active": True,
        }
    },
    "demo_product_vision": {
        "model": "product.product",
        "values": {
            "name": "Vision Alignment Camera",
            "active": True,
        }
    },
    "demo_version_gripper_v1": {
        "model": "product.version",
        "values": {
            "product_id": "@demo_product_gripper",
            "version": 1,
            "name": "Adaptive Gripper Head",
            "default_code": "AGH-001",
            "description": "Initial release of the adaptive gripper assembly.",
            "state": "active",
            "sale_price": 18500,
            "cost_price": 12600,
        }
    },
    "demo_version_power_v1": {
        "model": "product.version",
        "values": {
            "product_id": "@demo_product_power",
            "version": 1,
            "name": "Auxiliary Power Module",
            "default_code": "APM-001",
            "description": "24V regulated auxiliary power distribution module.",
            "state": "active",
            "sale_price": 2400,
            "cost_price": 1650,
        }
    },
    "demo_version_vision_v1": {
        "model": "product.version",
        "values": {
            "product_id": "@demo_product_vision",
            "version": 1,
            "name": "Vision Alignment Camera",
            "default_code": "VAC-001",
            "description": "Compact alignment camera for guided assembly stations.",
            "state": "active",
            "sale_price": 3200,
            "cost_price": 2100,
        }
    },

    # ── Demo: BOMs ─────────────────────────────────────────────────────────────
    # BOM for Main Controller Board — uses motor driver + sensor + wiring harness
    "demo_bom_controller": {
        "model": "mrp.bom",
        "values": {
            "name": "New",
            "product_version_id": "@demo_version_controller_v1",
            "version": 1,
            "state": "active",
            "notes": "BOM for Main Controller Board v1. Includes driver, sensor and harness.",
        }
    },
    # BOM for Servo Motor 24V — uses wiring harness + sensor
    "demo_bom_motor": {
        "model": "mrp.bom",
        "values": {
            "name": "New",
            "product_version_id": "@demo_version_motor_v1",
            "version": 1,
            "state": "active",
            "notes": "BOM for Servo Motor 24V v1.",
        }
    },
    # BOM for Robotic Arm Unit — uses controller, motor x4, frame, cable x2
    "demo_bom_arm": {
        "model": "mrp.bom",
        "values": {
            "name": "New",
            "product_version_id": "@demo_version_arm_v1",
            "version": 1,
            "state": "active",
            "notes": "Top-level BOM for Robotic Arm Unit v1.",
        }
    },
    "demo_bom_gripper": {
        "model": "mrp.bom",
        "values": {
            "product_version_id": "@demo_version_gripper_v1",
            "version": 1,
            "state": "active",
            "notes": "Adaptive gripper BOM with power distribution, camera alignment and harnessing.",
        }
    },

    # ── Demo: Work Center + Routing Operation ─────────────────────────────────
    "demo_work_center_electronics": {
        "model": "work.center",
        "values": {
            "name": "Electronics Assembly Cell",
        }
    },
    "demo_work_center_mechanical": {
        "model": "work.center",
        "values": {
            "name": "Mechanical Integration Bay",
        }
    },
    "demo_work_center_final": {
        "model": "work.center",
        "values": {
            "name": "Final Calibration Station",
        }
    },
    "demo_routing_workcenter_controller_assembly": {
        "model": "mrp.routing.workcenter",
        "values": {
            "bom_id": "@demo_bom_controller",
            "operation": "Controller Board Assembly",
            "work_center_id": "@demo_work_center_electronics",
            "duration_minutes": 45,
        }
    },
    "demo_routing_workcenter_arm_final_test": {
        "model": "mrp.routing.workcenter",
        "values": {
            "bom_id": "@demo_bom_arm",
            "operation": "Arm Final Integration Test",
            "work_center_id": "@demo_work_center_final",
            "duration_minutes": 70,
        }
    },
    "demo_routing_workcenter_gripper_assembly": {
        "model": "mrp.routing.workcenter",
        "values": {
            "bom_id": "@demo_bom_gripper",
            "operation": "Gripper Head Assembly",
            "work_center_id": "@demo_work_center_mechanical",
            "duration_minutes": 35,
        }
    },

    # ── Demo: BOM Lines ────────────────────────────────────────────────────────
    # Lines for BOM-MCB-001 (Main Controller Board)
    "demo_bom_line_mcb_driver": {
        "model": "mrp.bom.line",
        "values": {
            "bom_id": "@demo_bom_controller",
            "component_product_id": "@demo_version_driver_v1",
            "quantity": 1,
            "notes": "Dual H-bridge motor driver",
        }
    },
    "demo_bom_line_mcb_sensor": {
        "model": "mrp.bom.line",
        "values": {
            "bom_id": "@demo_bom_controller",
            "component_product_id": "@demo_version_sensor_v1",
            "quantity": 2,
            "notes": "Position feedback sensors",
        }
    },
    "demo_bom_line_mcb_cable": {
        "model": "mrp.bom.line",
        "values": {
            "bom_id": "@demo_bom_controller",
            "component_product_id": "@demo_version_cable_v1",
            "quantity": 1,
            "notes": "Internal wiring harness",
        }
    },

    # Lines for BOM-SM24-001 (Servo Motor 24V)
    "demo_bom_line_motor_sensor": {
        "model": "mrp.bom.line",
        "values": {
            "bom_id": "@demo_bom_motor",
            "component_product_id": "@demo_version_sensor_v1",
            "quantity": 1,
            "notes": "Shaft position sensor",
        }
    },
    "demo_bom_line_motor_cable": {
        "model": "mrp.bom.line",
        "values": {
            "bom_id": "@demo_bom_motor",
            "component_product_id": "@demo_version_cable_v1",
            "quantity": 1,
            "notes": "Power and signal harness",
        }
    },

    # Lines for BOM-RAU-001 (Robotic Arm Unit)
    "demo_bom_line_arm_controller": {
        "model": "mrp.bom.line",
        "values": {
            "bom_id": "@demo_bom_arm",
            "component_product_id": "@demo_version_controller_v1",
            "quantity": 1,
            "notes": "Main controller board",
        }
    },
    "demo_bom_line_arm_motor": {
        "model": "mrp.bom.line",
        "values": {
            "bom_id": "@demo_bom_arm",
            "component_product_id": "@demo_version_motor_v1",
            "quantity": 4,
            "notes": "Joint servo motors (one per axis)",
        }
    },
    "demo_bom_line_arm_frame": {
        "model": "mrp.bom.line",
        "values": {
            "bom_id": "@demo_bom_arm",
            "component_product_id": "@demo_version_frame_v1",
            "quantity": 1,
            "notes": "Structural aluminium frame",
        }
    },
    "demo_bom_line_arm_cable": {
        "model": "mrp.bom.line",
        "values": {
            "bom_id": "@demo_bom_arm",
            "component_product_id": "@demo_version_cable_v1",
            "quantity": 2,
            "notes": "External wiring harnesses",
        }
    },

    # Lines for Adaptive Gripper Head BOM
    "demo_bom_line_gripper_sensor": {
        "model": "mrp.bom.line",
        "values": {
            "bom_id": "@demo_bom_gripper",
            "component_product_id": "@demo_version_sensor_v1",
            "quantity": 2,
            "notes": "Finger position sensing modules",
        }
    },
    "demo_bom_line_gripper_power": {
        "model": "mrp.bom.line",
        "values": {
            "bom_id": "@demo_bom_gripper",
            "component_product_id": "@demo_version_power_v1",
            "quantity": 1,
            "notes": "Auxiliary power regulation board",
        }
    },
    "demo_bom_line_gripper_vision": {
        "model": "mrp.bom.line",
        "values": {
            "bom_id": "@demo_bom_gripper",
            "component_product_id": "@demo_version_vision_v1",
            "quantity": 1,
            "notes": "Alignment camera for precision pickup",
        }
    },
    "demo_bom_line_gripper_cable": {
        "model": "mrp.bom.line",
        "values": {
            "bom_id": "@demo_bom_gripper",
            "component_product_id": "@demo_version_cable_v1",
            "quantity": 1,
            "notes": "Control and power harness",
        }
    },

    # ── Demo: ECOs ────────────────────────────────────────────────────────────
    # Names are intentionally omitted so plm.eco.create() generates sequence values.
    "demo_eco_controller_refresh": {
        "model": "plm.eco",
        "values": {
            "type": "product",
            "product_id": "@demo_product_controller",
            "initiated_by_id": "@demo_user_engineering",
            "description": "Refresh the main controller board for higher current tolerance and improved connector routing.",
            "update_version": True,
            "eco_name": "Main Controller Board Rev A",
            "eco_default_code": "MCB-002",
            "eco_sale_price": 12800,
            "eco_cost_price": 9100,
            "eco_change_notes": "Upgrade copper weight, add keyed service connector, and reserve header space for firmware diagnostics."
        }
    },
    "demo_eco_arm_bom_upgrade": {
        "model": "plm.eco",
        "values": {
            "type": "bom",
            "bom_id": "@demo_bom_arm",
            "initiated_by_id": "@demo_user_engineering",
            "description": "Improve the robotic arm BOM with redundant sensing, auxiliary power distribution, and a dedicated calibration step.",
            "update_version": True,
            "eco_line_ids": {
                "create": [
                    {
                        "component_product_id": "@demo_version_sensor_v1",
                        "quantity": 6,
                        "notes": "Redundant position sensing for paired arm joints."
                    },
                    {
                        "component_product_id": "@demo_version_power_v1",
                        "quantity": 1,
                        "notes": "Dedicated auxiliary power distribution module."
                    },
                    {
                        "component_product_id": "@demo_version_cable_v1",
                        "quantity": 3,
                        "notes": "Additional harness capacity for calibration and diagnostics."
                    }
                ]
            },
            "eco_workorder_ids": {
                "create": [
                    {
                        "operation": "Harness Integrity Validation",
                        "work_center_id": "@demo_work_center_electronics",
                        "duration_minutes": 25
                    },
                    {
                        "operation": "Precision Joint Calibration",
                        "work_center_id": "@demo_work_center_final",
                        "duration_minutes": 60
                    }
                ]
            }
        }
    },
}
