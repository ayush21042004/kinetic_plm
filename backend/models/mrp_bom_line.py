from backend.core.znova_model import ZnovaModel
from backend.core import fields


class Line(ZnovaModel):
    __tablename__ = "mrp_bom_line"
    _model_name_ = "mrp.bom.line"
    _name_field_ = "component_product_id"
    _description_ = "BoM Component Line"

    bom_id = fields.Many2one(
        "mrp.bom", label="Bill of Materials", required=True, ondelete="cascade"
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
            "fields": ["bom_id", "component_product_id", "quantity"],
            "search_fields": ["component_product_id"]
        },
        "form": {
            "groups": [
                {"title": "Component", "fields": ["bom_id", "component_product_id", "quantity"]},
                {"title": "Notes",     "fields": ["notes"]},
            ]
        }
    }
