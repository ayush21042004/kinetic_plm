from backend.core.znova_model import ZnovaModel
from backend.core import fields


class EcoStageLine(ZnovaModel):
    __tablename__ = "plm_eco_stage_line"
    _model_name_ = "plm.eco.stage.line"
    _name_field_ = "user_id"
    _description_ = "ECO Stage Approval Line"

    stage_id = fields.Many2one("plm.eco.stage", label="Stage", required=True)
    user_id = fields.Many2one("user", label="Approver", required=True, tracking=True)
    approval_required = fields.Boolean(
        label="Approval Required",
        default=True,
        tracking=True,
        help="If checked, this user must approve before the ECO can move past this stage."
    )

    _role_permissions = {
        "admin":       {"create": True,  "read": True, "write": True,  "delete": True,  "domain": []},
        "engineering": {"create": False, "read": True, "write": False, "delete": False, "domain": []},
        "approver":    {"create": False, "read": True, "write": False, "delete": False, "domain": []},
        "operations":  {"create": False, "read": True, "write": False, "delete": False, "domain": []},
    }

    _ui_views = {
        "list": {
            "fields": ["user_id", "approval_required"],
            "search_fields": ["user_id"]
        },
        "form": {
            "groups": [
                {"title": "Approval Rule", "fields": ["stage_id", "user_id", "approval_required"]},
            ]
        }
    }
