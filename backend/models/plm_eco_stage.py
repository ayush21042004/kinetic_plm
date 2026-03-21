from sqlalchemy.orm import Session
from backend.core.znova_model import ZnovaModel
from backend.core import fields
from backend.core.exceptions import ValidationError


class EcoStage(ZnovaModel):
    __tablename__ = "plm_eco_stage"
    _model_name_ = "plm.eco.stage"
    _name_field_ = "name"
    _description_ = "ECO Stage"

    name = fields.Char(label="Stage Name", required=True, size=100, tracking=True)
    sequence = fields.Integer(label="Sequence", default=10, tracking=True)
    is_last_stage = fields.Boolean(label="Last Stage", default=False, tracking=True,
                                   help="Only one stage can be marked as the last stage. ECOs in this stage will not show the 'Send for Approval' button.")

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

    @classmethod
    def _ensure_single_last_stage(cls, db: Session, is_last: bool, exclude_id=None):
        """Raise if trying to set is_last_stage=True when another stage already has it."""
        if not is_last:
            return
        from backend.core.base_model import Environment
        env = Environment(db)
        domain = [("is_last_stage", "=", True)]
        existing = env["plm.eco.stage"].search(domain, limit=1)
        if existing:
            stage = existing[0]
            if exclude_id is None or stage.id != exclude_id:
                raise ValidationError(
                    f"Stage '{stage.name}' is already marked as the last stage. "
                    "Only one stage can be the last stage."
                )

    @classmethod
    def create(cls, db: Session, vals: dict):
        cls._ensure_single_last_stage(db, vals.get("is_last_stage", False))
        return super().create(db, vals)

    def write(self, *args, **kwargs):
        vals = args[1] if len(args) == 2 else (args[0] if args else kwargs)
        db = args[0] if len(args) == 2 else None
        if db is None:
            from sqlalchemy.orm import object_session
            db = object_session(self)
        if db and vals.get("is_last_stage", False):
            self.__class__._ensure_single_last_stage(db, True, exclude_id=self.id)
        return super().write(*args, **kwargs)

    _ui_views = {
        "list": {
            "fields": ["name", "sequence", "is_last_stage"],
            "search_fields": ["name"]
        },
        "form": {
            "groups": [
                {"title": "Stage Name", "fields": ["name"], "position": "header"},
                {"title": "Settings", "fields": ["sequence", "is_last_stage"]},
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
