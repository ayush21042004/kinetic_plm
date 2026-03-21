from backend.core.znova_model import ZnovaModel
from backend.core import fields


class Product(ZnovaModel):
    __tablename__ = "product_product"
    _model_name_ = "product.product"
    _name_field_ = "name"
    _description_ = "Product"

    name = fields.Char(label="Product Name", required=True, size=200, tracking=True)
    active = fields.Boolean(label="Active", default=True)

    current_version_id = fields.Many2one(
        "product.version",
        label="Current Version",
        readonly=True,
        help="The currently active version of this product."
    )

    version_ids = fields.One2many(
        "product.version", "product_id",
        label="Versions",
        columns=["version", "name", "default_code", "state", "sale_price"]
    )

    _role_permissions = {
        "admin":       {"create": True,  "read": True, "write": True,  "delete": True,  "domain": []},
        "engineering": {"create": True,  "read": True, "write": True,  "delete": False, "domain": []},
        "approver":    {"create": False, "read": True, "write": False, "delete": False, "domain": []},
        "operations":  {"create": False, "read": True, "write": False, "delete": False, "domain": []},
    }

    _ui_views = {
        "list": {
            "fields": ["name", "current_version_id", "active"],
            "search_fields": ["name"]
        },
        "form": {
            "show_audit_log": True,
            "groups": [
                {"title": "Product Name", "fields": ["name"], "position": "header"},
            ],
            "tabs": [
                {
                    "title": "General",
                    "groups": [
                        {
                            "title": "Product Details",
                            "fields": ["active"]
                        },
                        {
                            "title": "Current Version",
                            "fields": ["current_version_id"]
                        }
                    ]
                },
                {
                    "title": "Versions",
                    "fields": ["version_ids"]
                }
            ]
        }
    }
