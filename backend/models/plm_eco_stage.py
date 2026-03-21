from backend.core.znova_model import ZnovaModel
from backend.core import fields


class EcoStage(ZnovaModel):
    __tablename__ = "plm_eco_stage"
    _model_name_ = "plm.eco.stage"
    _name_field_ = "name"
    _description_ = "ECO Stage"

    name = fields.Char(label="Stage Name", required=True, size=100, tracking=True)
    sequence = fields.Integer(label="Sequence", default=10, tracking=True)

    # Approval lines for this stage
    approval_line_ids = fields.One2many(
        "plm.eco.stage.line", "stage_id",
        label="Approval Rules",
        columns=["user_id", "approval_required"],
    )

    _role_permissions = {
        "admin":       {"create": True,  "read": True, "write": True,  "delete": True,  "domain": []},
        "engineering": {"create": False, "read": True, "write": False, "delete": False, "domain": []},
        "approver":    {"create": False, "read": True, "write": False, "delete": False, "domain": []},
        "operations":  {"create": False, "read": True, "write": False, "delete": False, "domain": []},
    }

    _ui_views = {
        "list": {
            "fields": ["name", "sequence", "fold"],
            "search_fields": ["name"]
        },
        "form": {
            "groups": [
                {"title": "Stage Name", "fields": ["name"], "position": "header"},
                {"title": "Settings", "fields": ["sequence"]},
            ],
            "tabs": [
                {
                    "title": "Approval Rules",
                    "groups": [
                        {
                            "title": "Approvers",
                            "fields": ["approval_line_ids"]
                        }
                    ]
                }
            ]
        }
    }
