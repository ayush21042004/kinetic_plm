RECORDS = {
    # ── Roles ──────────────────────────────────────────────────────────────────

    "role_admin": {
        "model": "role",
        "values": {
            "name": "admin",
            "description": "Full access. Configures ECO stages, approval rules, and manages master data settings."
        },
        "noupdate": True
    },
    "role_engineering": {
        "model": "role",
        "values": {
            "name": "engineering",
            "description": "Creates and modifies ECOs, proposes Product/BoM changes, works on draft versions, and initiates approval workflows."
        },
        "noupdate": True
    },
    "role_approver": {
        "model": "role",
        "values": {
            "name": "approver",
            "description": "Reviews proposed changes, approves/validates ECOs based on stage rules, and controls when changes become effective."
        },
        "noupdate": True
    },
    "role_operations": {
        "model": "role",
        "values": {
            "name": "operations",
            "description": "View-only access to active Products and Bills of Materials."
        },
        "noupdate": True
    },

    # ── Admin User ─────────────────────────────────────────────────────────────

    "user_admin": {
        "model": "user",
        "values": {
            "email": "admin@kinetic.com",
            "full_name": "Administrator",
            "hashed_password": "$P$admin123",
            "role_id": "@role_admin",
            "timezone_id": "@tz_utc",
            "is_active": True
        },
        "noupdate": True
    },
}
