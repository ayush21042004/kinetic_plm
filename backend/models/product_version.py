from backend.core.znova_model import ZnovaModel
from backend.core import fields, api


class Version(ZnovaModel):
    __tablename__ = "product_version"
    _model_name_ = "product.version"
    _name_field_ = "name"
    _description_ = "Product Version"

    product_id = fields.Many2one(
        "product.product", label="Product", tracking=True
    )
    version = fields.Integer(label="Version Number", required=True, default=1, tracking=True, readonly=True)
    name = fields.Char(label="Product Name", required=True, size=200, tracking=True,
                       help="e.g. v1.0, v2.1-stable")
    default_code = fields.Char(label="Internal Reference", size=100, tracking=True)
    description = fields.Text(label="Change Notes")

    state = fields.Selection([
        ("draft",    "Draft"),
        ("active",   "Active"),
        ("archived", "Archived"),
    ], label="State", default="draft", tracking=True, options={
        "draft":    {"label": "Draft",    "color": "info"},
        "active":   {"label": "Active",   "color": "success"},
        "archived": {"label": "Archived", "color": "secondary"},
    })

    sale_price = fields.Integer(label="Sale Price", default=0, tracking=True)
    cost_price = fields.Integer(label="Cost Price", default=0, tracking=True)

    bom_id = fields.Many2one("mrp.bom", label="Bill of Materials", readonly=True)
    eco_id = fields.Many2one("plm.eco", label="Source ECO", readonly=True)

    attachments = fields.Attachments(
        label="Attachments",
        allowed_types=["pdf", "doc", "docx", "png", "jpg", "jpeg", "xlsx", "csv"],
        max_size=10485760
    )

    bom_count = fields.Integer(label="BoM", compute="_compute_bom_count", store=True)
    eco_count = fields.Integer(label="ECO", compute="_compute_eco_count", store=True)

    _role_permissions = {
        "admin":       {"create": True,  "read": True, "write": True,  "delete": True,  "domain": []},
        "engineering": {"create": True,  "read": True, "write": True,  "delete": False, "domain": []},
        "approver":    {"create": False, "read": True, "write": False, "delete": False, "domain": []},
        "operations":  {"create": False, "read": True, "write": False, "delete": False, "domain": []},
    }

    _search_config = {
        "filters": [
            {"name": "draft",    "label": "Draft",    "domain": "[('state', '=', 'draft')]"},
            {"name": "active",   "label": "Active",   "domain": "[('state', '=', 'active')]"},
            {"name": "archived", "label": "Archived", "domain": "[('state', '=', 'archived')]"},
        ],
        "group_by": [
            {"name": "by_product", "label": "By Product", "field": "product_id"},
            {"name": "by_state",   "label": "By State",   "field": "state"},
        ]
    }

    _ui_views = {
        "list": {
            "fields": ["name", "version", "default_code", "state", "sale_price", "cost_price"],
            "search_fields": ["name", "product_id", "default_code"]
        },
        "form": {
            "show_audit_log": True,
            "smart_buttons": [
                {
                    "name": "bom",
                    "label": "Bill of Materials",
                    "icon": "Layers",
                    "field": "bom_count",
                    "method": "action_view_bom",
                    "invisible": "[('bom_id', '=', false)]"
                },
                {
                    "name": "eco",
                    "label": "ECO",
                    "icon": "GitBranch",
                    "field": "eco_count",
                    "method": "action_view_eco",
                    "invisible": "[('eco_id', '=', false)]"
                }
            ],
            "groups": [
                {"title": "Version Name", "fields": ["name"], "position": "header"},
            ],
            "tabs": [
                {
                    "title": "General",
                    "groups": [
                        {
                            "title": "Identity",
                            "fields": ["version", "default_code"]
                        },
                        {
                            "title": "Pricing",
                            "fields": ["sale_price", "cost_price"]
                        },
                        {
                            "title": "Change Notes",
                            "fields": ["description"]
                        }
                    ]
                },
                {
                    "title": "Attachments",
                    "groups": [
                        {
                            "title": "Files",
                            "fields": ["attachments"]
                        }
                    ]
                }
            ]
        }
    }

    @classmethod
    def create(cls, db, vals: dict):
        """
        Auto-create a product.product with the same name if product_id is not provided,
        then after version is created, set product.current_version_id to this version.
        """
        env = cls.get_env(db)

        # If no product linked, create one automatically
        if not vals.get("product_id"):
            product = env["product.product"].create({
                "name": vals.get("name", "New Product"),
            })
            vals["product_id"] = product.id
        else:
            product = env["product.product"].search(
                [("id", "=", vals["product_id"])], limit=1
            )

        # Create the version record
        version = super().create(db, vals)

        # Set current_version_id on the product to this new version
        if product:
            product.write({"current_version_id": version.id})

        return version

    @api.depends("bom_id")
    def _compute_bom_count(self):
        self.bom_count = 1 if self.bom_id else 0

    @api.depends("eco_id")
    def _compute_eco_count(self):
        self.eco_count = 1 if self.eco_id else 0

    def action_view_bom(self):
        if not self.bom_id:
            return {}
        return {
            "type": "ir.actions.act_window",
            "res_model": "mrp.bom",
            "view_mode": "form",
            "res_id": self.bom_id.id,
            "name": f"BoM for {self.name}"
        }

    def action_view_eco(self):
        if not self.eco_id:
            return {}
        return {
            "type": "ir.actions.act_window",
            "res_model": "plm.eco",
            "view_mode": "form",
            "res_id": self.eco_id.id,
            "name": f"ECO for {self.name}"
        }
