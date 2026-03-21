from backend.core.znova_model import ZnovaModel
from backend.core import fields


class EcoLine(ZnovaModel):
    __tablename__ = "plm_eco_line"
    _model_name_ = "plm.eco.line"
    _name_field_ = "component_product_id"
    _description_ = "ECO BoM Component Line"

    eco_id = fields.Many2one(
        "plm.eco", label="ECO", required=True, ondelete="cascade"
    )
    component_product_id = fields.Many2one(
        "product.version", label="Component Version", required=True, tracking=True
    )
    quantity = fields.Integer(label="Quantity", required=True, default=1, tracking=True)
    notes = fields.Text(label="Notes")

    _role_permissions = {
        "admin":       {"create": True,  "read": True, "write": True,  "delete": True,  "domain": []},
        "engineering": {"create": True,  "read": True, "write": True,  "delete": True,  "domain": []},
        "approver":    {"create": False, "read": True, "write": False, "delete": False, "domain": []},
        "operations":  {"create": False, "read": True, "write": False, "delete": False, "domain": []},
    }

    _ui_views = {
        "list": {
            "fields": ["component_product_id", "quantity", "notes"],
            "search_fields": ["component_product_id"]
        },
        "form": {
            "groups": [
                {"title": "Component", "fields": ["eco_id", "component_product_id", "quantity"]},
                {"title": "Notes",     "fields": ["notes"]},
            ]
        }
    }
