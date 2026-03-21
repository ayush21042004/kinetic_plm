from backend.core.znova_model import ZnovaModel
from backend.core import fields
from backend.core.exceptions import UserError


class EcoStageLine(ZnovaModel):
    __tablename__ = "plm_eco_stage_line"
    _model_name_ = "plm.eco.stage.line"
    _name_field_ = "user_id"
    _description_ = "ECO Stage Approval Line"

    stage_id = fields.Many2one("plm.eco.stage", label="Stage", required=True)
    user_id = fields.Many2one(
        "user", 
        label="Approver", 
        required=True, 
        tracking=True,
        domain="[('role_id.name', '=', 'approver')]"
    )
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

    def _check_duplicate_approver(self, db, stage_id, user_id):
        if not stage_id or not user_id:
            return
        
        # Check if this user already exists in this stage
        # Need to exclude current record during write
        domain = [('stage_id', '=', stage_id), ('user_id', '=', user_id)]
        if self.id:
            domain.append(('id', '!=', self.id))
            
        existing = self.search(domain, db=db)
        if existing:
            from backend.models.user import User
            user_record = User.browse(user_id, db=db)
            raise UserError(f"User '{user_record.full_name}' is already an approver in this stage.")

    @classmethod
    def create(cls, db, vals):
        # We need a dummy instance to call _check_duplicate_approver
        dummy = cls() 
        dummy._check_duplicate_approver(db, vals.get('stage_id'), vals.get('user_id'))
        return super().create(db, vals)

    def write(self, *args, **kwargs):
        vals = args[1] if len(args) == 2 else (args[0] if args else kwargs)
        db = args[0] if len(args) == 2 else None
        if db is None:
            from sqlalchemy.orm import object_session
            db = object_session(self)
        
        if 'user_id' in vals or 'stage_id' in vals:
            # Use current values as fallback if not being updated
            new_user_id = vals.get('user_id', self.user_id)
            new_stage_id = vals.get('stage_id', self.stage_id)
            self._check_duplicate_approver(db, new_stage_id, new_user_id)
            
        return super().write(*args, **kwargs)

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
