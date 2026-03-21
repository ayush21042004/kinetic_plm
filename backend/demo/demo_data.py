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
}
