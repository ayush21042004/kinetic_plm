from backend.core.znova_model import ZnovaModel
from backend.core import fields


class EcoApproval(ZnovaModel):
    __tablename__ = "plm_eco_approval"
    _model_name_ = "plm.eco.approval"
    _name_field_ = "user_id"
    _description_ = "ECO Stage Approval Tracking"

    eco_id = fields.Many2one("plm.eco", label="ECO", required=True, tracking=True)
    stage_id = fields.Many2one("plm.eco.stage", label="Stage", required=True, tracking=True)
    user_id = fields.Many2one("user", label="Approver", required=True, tracking=True)
    approval_required = fields.Boolean(
        label="Approval Required",
        default=True,
        tracking=True,
        help="If checked, this approval blocks moving the ECO to the next stage."
    )
    approval_time = fields.DateTime(
        label="Approval Time",
        readonly=True,
        tracking=True,
        help="Timestamp when the approver approved this ECO stage."
    )
    approved = fields.Boolean(
        label="Approved",
        default=False,
        tracking=True,
        help="Whether this approver has approved the ECO for this stage."
    )

    @classmethod
    def run_approval_reminders(cls, db):
        """
        Cron job: Send reminders for pending approvals.
        """
        from backend.services.approval_reminder_service import get_approval_reminder_service
        service = get_approval_reminder_service(db)
        return service.run_reminders()

    _role_permissions = {
        "admin":       {"create": True,  "read": True, "write": True,  "delete": True,  "domain": []},
        "engineering": {"create": False, "read": True, "write": False, "delete": False, "domain": []},
        "approver":    {"create": False, "read": True, "write": True,  "delete": False, "domain": [("user_id", "=", "user.id")]},
        "operations":  {"create": False, "read": True, "write": False, "delete": False, "domain": []},
    }

    _ui_views = {
        "list": {
            "fields": ["eco_id", "stage_id", "user_id", "approval_required", "approved", "approval_time"],
            "search_fields": ["eco_id", "stage_id", "user_id"]
        },
        "form": {
            "groups": [
                {
                    "title": "Approval",
                    "fields": ["eco_id", "stage_id", "user_id", "approval_required", "approved", "approval_time"]
                }
            ]
        }
    }
