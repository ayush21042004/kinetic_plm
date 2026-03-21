from backend.core.znova_model import ZnovaModel
from backend.core import fields
from backend.core.exceptions import UserError


class Eco(ZnovaModel):
    __tablename__ = "plm_eco"
    _model_name_ = "plm.eco"
    _name_field_ = "name"
    _description_ = "Engineering Change Order"

    name = fields.Char(label="ECO Reference", required=True, size=100, tracking=True,
                       help="e.g. ECO-2024-001")

    type = fields.Selection([
        ("product", "Product"),
        ("bom",     "BoM"),
    ], label="ECO Type", required=True, default="product", tracking=True, options={
        "product": {"label": "Product", "color": "primary"},
        "bom":     {"label": "BoM",     "color": "info"},
    })

    state = fields.Selection([
        ("draft",     "Draft"),
        ("in_review", "In Review"),
        ("approved",  "Approved"),
        ("done",      "Done"),
    ], label="State", default="draft", tracking=True, options={
        "draft":     {"label": "Draft",     "color": "secondary"},
        "in_review": {"label": "In Review", "color": "warning"},
        "approved":  {"label": "Approved",  "color": "success"},
        "done":      {"label": "Done",      "color": "primary"},
    })

    description = fields.Text(label="Description", tracking=True)
    update_version = fields.Boolean(label="Update Version", default=True, tracking=True)
    initiated_by_id = fields.Many2one("user", label="Initiated By", default="current_user", tracking=True)

    # Shown in top form, hidden based on type
    product_id = fields.Many2one(
        "product.product", label="Product",
        invisible="[('type', '!=', 'product')]",
        required="[('type', '=', 'product')]",
        tracking=True
    )
    bom_id = fields.Many2one(
        "mrp.bom", label="Target BoM",
        invisible="[('type', '!=', 'bom')]",
        required="[('type', '=', 'bom')]",
        tracking=True
    )

    # Product ECO change fields
    eco_name = fields.Char(label="Product Name", size=200, tracking=True,
                           invisible="[('type', '!=', 'product')]")
    eco_default_code = fields.Char(label="Internal Reference", size=100, tracking=True,
                                   invisible="[('type', '!=', 'product')]")
    eco_sale_price = fields.Integer(label="Sale Price", default=0, tracking=True,
                                    invisible="[('type', '!=', 'product')]")
    eco_cost_price = fields.Integer(label="Cost Price", default=0, tracking=True,
                                    invisible="[('type', '!=', 'product')]")
    eco_attachments = fields.Attachments(
        label="Attachments",
        allowed_types=["pdf", "doc", "docx", "png", "jpg", "jpeg", "xlsx", "csv"],
        max_size=10485760,
        invisible="[('type', '!=', 'product')]"
    )

    # BoM ECO change fields
    eco_line_ids = fields.One2many(
        "plm.eco.line", "eco_id",
        label="Proposed Components",
        columns=["component_product_id", "quantity", "notes"],
        invisible="[('type', '!=', 'bom')]"
    )

    _role_permissions = {
        "admin":       {"create": True,  "read": True, "write": True,  "delete": True,  "domain": []},
        "engineering": {"create": True,  "read": True, "write": True,  "delete": False, "domain": []},
        "approver":    {"create": False, "read": True, "write": True,  "delete": False, "domain": []},
        "operations":  {"create": False, "read": True, "write": False, "delete": False, "domain": []},
    }

    _search_config = {
        "filters": [
            {"name": "draft",       "label": "Draft",        "domain": "[('state', '=', 'draft')]"},
            {"name": "in_review",   "label": "In Review",    "domain": "[('state', '=', 'in_review')]"},
            {"name": "approved",    "label": "Approved",     "domain": "[('state', '=', 'approved')]"},
            {"name": "done",        "label": "Done",         "domain": "[('state', '=', 'done')]"},
            {"name": "product_eco", "label": "Product ECOs", "domain": "[('type', '=', 'product')]"},
            {"name": "bom_eco",     "label": "BoM ECOs",     "domain": "[('type', '=', 'bom')]"},
        ],
        "group_by": [
            {"name": "by_type",  "label": "By Type",      "field": "type"},
            {"name": "by_state", "label": "By State",     "field": "state"},
            {"name": "by_user",  "label": "By Initiator", "field": "initiated_by_id"},
        ]
    }

    _ui_views = {
        "list": {
            "fields": ["name", "type", "state", "product_id", "bom_id", "initiated_by_id"],
            "search_fields": ["name", "type", "state"]
        },
        "form": {
            "show_audit_log": True,
            "groups": [
                {"title": "ECO Reference", "fields": ["name"], "position": "header"},
                {
                    "title": "ECO Identity",
                    "fields": ["type", "initiated_by_id", "product_id", "bom_id"]
                },
                {
                    "title": "Description",
                    "fields": ["update_version", "description"]
                }
            ],
            "tabs": [
                {
                    "title": "Product Change",
                    "invisible": "[('type', '!=', 'product')]",
                    "groups": [
                        {
                            "title": "Product Details",
                            "fields": ["eco_name", "eco_default_code", "eco_sale_price", "eco_cost_price"]
                        },
                        {
                            "title": "Attachments",
                            "fields": ["eco_attachments"]
                        }
                    ]
                },
                {
                    "title": "BoM Change",
                    "invisible": "[('type', '!=', 'bom')]",
                    "groups": [
                        {
                            "title": "Proposed Components",
                            "fields": ["eco_line_ids"]
                        }
                    ]
                }
            ]
        }
    }

    @classmethod
    def _validate_type_required(cls, vals: dict):
        eco_type = vals.get("type")
        if not eco_type:
            return
        if eco_type == "product" and not vals.get("product_id"):
            raise UserError("Product is required for a Product ECO.")
        if eco_type == "bom" and not vals.get("bom_id"):
            raise UserError("Target BoM is required for a BoM ECO.")

    @classmethod
    def create(cls, db, vals: dict):
        # Unwrap Many2one dicts
        for f in ("product_id", "bom_id"):
            if isinstance(vals.get(f), dict):
                vals[f] = vals[f].get("id")
        cls._validate_type_required(vals)
        return super().create(db, vals)

    def write(self, *args, **kwargs):
        vals = args[1] if len(args) == 2 else (args[0] if args else kwargs)
        for f in ("product_id", "bom_id"):
            if isinstance(vals.get(f), dict):
                vals[f] = vals[f].get("id")
        # Merge with current values to validate the final state
        merged = {
            "type":       vals.get("type", self.type),
            "product_id": vals.get("product_id", self.product_id.id if self.product_id else None),
            "bom_id":     vals.get("bom_id", self.bom_id.id if self.bom_id else None),
        }
        self._validate_type_required(merged)
        return super().write(*args, **kwargs)
