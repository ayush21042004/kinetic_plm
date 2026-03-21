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

    # ── Demo: BOMs ─────────────────────────────────────────────────────────────
    # BOM for Main Controller Board — uses motor driver + sensor + wiring harness
    "demo_bom_controller": {
        "model": "mrp.bom",
        "values": {
            "name": "BOM-MCB-001",
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
            "name": "BOM-SM24-001",
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
            "name": "BOM-RAU-001",
            "product_version_id": "@demo_version_arm_v1",
            "version": 1,
            "state": "active",
            "notes": "Top-level BOM for Robotic Arm Unit v1.",
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
}
