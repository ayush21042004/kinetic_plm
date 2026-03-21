from backend.core.znova_model import ZnovaModel
from backend.core import fields


class WorkCenter(ZnovaModel):
    __tablename__ = "work_center"
    _model_name_ = "work.center"
    _name_field_ = "name"
    _description_ = "Work Center"

    name = fields.Char(label="Work Center", required=True, size=200, tracking=True)
    routing_line_ids = fields.One2many(
        "mrp.routing.workcenter", "work_center_id",
        label="Routing Operations",
        columns=["bom_id", "operation", "duration_minutes"],
        show_label=False,
    )

    _role_permissions = {
        "admin":       {"create": True,  "read": True, "write": True,  "delete": True,  "domain": []},
        "engineering": {"create": True,  "read": True, "write": True,  "delete": False, "domain": []},
        "approver":    {"create": False, "read": True, "write": False, "delete": False, "domain": []},
        "operations":  {"create": False, "read": True, "write": False, "delete": False, "domain": []},
    }

    _ui_views = {
        "list": {
            "fields": ["name"],
            "search_fields": ["name"]
        },
        "form": {
            "show_audit_log": True,
            "groups": [
                {"title": "Work Center", "fields": ["name"], "position": "header"},
            ],
            "tabs": [
                {
                    "title": "Work Orders",
                    "fields": ["routing_line_ids"]
                }
            ]
        }
    }
