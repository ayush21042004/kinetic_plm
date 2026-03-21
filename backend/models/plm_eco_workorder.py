from backend.core.znova_model import ZnovaModel
from backend.core import fields


class EcoWorkorder(ZnovaModel):
    __tablename__ = "plm_eco_workorder"
    _model_name_ = "plm.eco.workorder"
    _name_field_ = "operation"
    _description_ = "ECO BoM Work Order"

    eco_id = fields.Many2one(
        "plm.eco", label="ECO", required=True, ondelete="cascade"
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
        "engineering": {"create": True,  "read": True, "write": True,  "delete": True,  "domain": []},
        "approver":    {"create": False, "read": True, "write": False, "delete": False, "domain": []},
        "operations":  {"create": False, "read": True, "write": False, "delete": False, "domain": []},
    }

    _ui_views = {
        "list": {
            "fields": ["operation", "work_center_id", "duration_minutes"],
            "search_fields": ["operation", "work_center_id"]
        },
        "form": {
            "groups": [
                {"title": "Work Order", "fields": ["eco_id", "operation", "work_center_id", "duration_minutes"]},
            ]
        }
    }
