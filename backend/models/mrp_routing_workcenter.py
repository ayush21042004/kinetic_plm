from backend.core.znova_model import ZnovaModel
from backend.core import fields


class RoutingWorkcenter(ZnovaModel):
    __tablename__ = "mrp_routing_workcenter"
    _model_name_ = "mrp.routing.workcenter"
    _name_field_ = "operation"
    _description_ = "BoM Routing Operation"

    bom_id = fields.Many2one(
        "mrp.bom", label="Bill of Materials", required=True, ondelete="cascade"
    )
    operation = fields.Char(label="Operation", required=True, size=200, tracking=True)
    work_center_id = fields.Many2one(
        "work.center", label="Work Center", required=True, tracking=True
    )
    duration_minutes = fields.Integer(
        label="Duration (Minutes)", required=True, default=0, tracking=True
    )

    _role_permissions = {
        "admin":       {"create": True,  "read": True, "write": True,  "delete": True,  "domain": []},
        "engineering": {"create": True,  "read": True, "write": True,  "delete": False, "domain": []},
        "approver":    {"create": False, "read": True, "write": False, "delete": False, "domain": []},
        "operations":  {"create": False, "read": True, "write": False, "delete": False, "domain": []},
    }

    _ui_views = {
        "list": {
            "fields": ["bom_id", "operation", "work_center_id", "duration_minutes"],
            "search_fields": ["operation", "work_center_id"]
        },
        "form": {
            "show_audit_log": True,
            "groups": [
                {
                    "title": "Operation",
                    "fields": ["bom_id", "operation", "work_center_id", "duration_minutes"]
                }
            ]
        }
    }
