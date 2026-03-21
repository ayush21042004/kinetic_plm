from backend.core.znova_model import ZnovaModel
from backend.core import fields, api


class Version(ZnovaModel):
    __tablename__ = "product_version"
    _model_name_ = "product.version"
    _name_field_ = "name"
    _description_ = "Product Version"

    product_id = fields.Many2one(
        "product.product", label="Product", tracking=True,
        readonly="[('state', 'in', ['active', 'archived'])]"
    )
    version = fields.Integer(label="Version Number", required=True, default=1, tracking=True, readonly=True)
    name = fields.Char(label="Product Name", required=True, size=200, tracking=True,
                       help="e.g. v1.0, v2.1-stable",
                       readonly="[('state', 'in', ['active', 'archived'])]")
    default_code = fields.Char(label="Internal Reference", size=100, tracking=True,
                               readonly="[('state', 'in', ['active', 'archived'])]")
    description = fields.Text(label="Change Notes",
                              readonly="[('state', 'in', ['active', 'archived'])]")

    state = fields.Selection([
        ("draft",    "Draft"),
        ("active",   "Active"),
        ("archived", "Archived"),
    ], label="State", default="draft", tracking=True, readonly=True, options={
        "draft":    {"label": "Draft",    "color": "info"},
        "active":   {"label": "Active",   "color": "success"},
        "archived": {"label": "Archived", "color": "secondary"},
    })

    sale_price = fields.Integer(label="Sale Price", default=0, tracking=True,
                                readonly="[('state', 'in', ['active', 'archived'])]")
    cost_price = fields.Integer(label="Cost Price", default=0, tracking=True,
                                readonly="[('state', 'in', ['active', 'archived'])]")

    bom_id = fields.Many2one("mrp.bom", label="Bill of Materials", readonly=True)
    eco_id = fields.Many2one("plm.eco", label="Source ECO", readonly=True)

    attachments = fields.Attachments(
        label="Attachments",
        allowed_types=["pdf", "doc", "docx", "png", "jpg", "jpeg", "xlsx", "csv"],
        max_size=10485760,
        readonly="[('state', 'in', ['active', 'archived'])]"
    )

    bom_count = fields.Integer(label="BoM", compute="_compute_bom_count", store=True)
    eco_count = fields.Integer(label="ECO", compute="_compute_eco_count", store=True)
    comparison_count = fields.Integer(label="Compare", compute="_compute_comparison_count", store=False)

    _role_permissions = {
        "admin":       {"create": True,  "read": True, "write": True,  "delete": True,  "domain": []},
        "engineering": {"create": True,  "read": True, "write": True,  "delete": False, "domain": []},
        "approver":    {"create": False, "read": True, "write": False, "delete": False, "domain": []},
        "operations":  {"create": False, "read": True, "write": False, "delete": False, "domain": []},
    }

    _search_config = {
        "filters": [
            {"name": "draft",    "label": "Draft",    "domain": "[('state', '=', 'draft')]"},
            {"name": "active",   "label": "Active",   "domain": "[('state', '=', 'active')]", "default": True},
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
            "header_buttons": [
                {
                    "name": "set_active",
                    "label": "Set Active",
                    "type": "primary",
                    "method": "action_set_active",
                    "invisible": "[('state', '=', 'active')]"
                },
                {
                    "name": "set_archived",
                    "label": "Archive",
                    "type": "secondary",
                    "method": "action_set_archived",
                    "invisible": "[('state', '=', 'archived')]"
                },
                {
                    "name": "reset_draft",
                    "label": "Reset to Draft",
                    "type": "warning",
                    "method": "action_reset_draft",
                    "invisible": "[('state', '=', 'draft')]"
                }
            ],
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
                },
                {
                    "name": "compare_versions",
                    "label": "Compare Versions",
                    "icon": "GitCompare",
                    "field": "comparison_count",
                    "method": "action_open_comparison",
                    "invisible": "[('comparison_count', '=', 0)]"
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

    @api.depends("product_id")
    def _compute_comparison_count(self):
        self.comparison_count = len(self._get_other_versions())

    def _comparison_field_labels(self):
        return {
            "name": "Product Name",
            "default_code": "Internal Reference",
            "description": "Change Notes",
            "sale_price": "Sale Price",
            "cost_price": "Cost Price",
            "attachments": "Attachments",
        }

    def _serialize_comparison_value(self, value):
        if value is None:
            return "-"
        if isinstance(value, list):
            # Handle attachment lists — extract filenames
            names = []
            for item in value:
                if isinstance(item, dict):
                    names.append(item.get("name") or item.get("filename") or str(item))
                elif hasattr(item, "name"):
                    names.append(item.name)
                else:
                    names.append(str(item))
            return ", ".join(names) if names else "-"
        return value

    def _get_attachments(self):
        """Manually fetch attachments since it's a virtual field."""
        from backend.core.registry import registry
        db = self._get_db()
        attachment_model = registry.get_model("ir.attachment")
        if not db or not attachment_model or not self.id:
            return []
        
        attachments = db.query(attachment_model).filter(
            attachment_model.res_model == self._model_name_,
            attachment_model.res_id == self.id,
            attachment_model.res_field == "attachments"
        ).all()
        
        # Return as list of dicts for comparison
        return [{"id": a.id, "name": a.name} for a in attachments]

    def _get_other_versions(self):
        from backend.core.base_model import Environment

        db = self._get_db()
        if not db or not self.product_id:
            return []

        env = Environment(db)
        versions = env["product.version"].search(
            [("product_id", "=", self.product_id.id), ("id", "!=", self.id)],
            order="version desc"
        )
        return list(getattr(versions, "_records", versions or []))

    def build_comparison_with(self, other_version):
        field_changes = []
        changed_count = 0

        for field_name, label in self._comparison_field_labels().items():
            if field_name == "attachments":
                old_value = other_version._get_attachments()
                new_value = self._get_attachments()
            else:
                old_value = getattr(other_version, field_name, None)
                new_value = getattr(self, field_name, None)

            if old_value != new_value:
                changed_count += 1
                field_changes.append({
                    "field": field_name,
                    "label": label,
                    "old_value": self._serialize_comparison_value(old_value),
                    "new_value": self._serialize_comparison_value(new_value),
                    "change_type": "updated",
                })

        return {
            "target": {
                "id": other_version.id,
                "name": other_version.name,
                "version": other_version.version,
                "state": other_version.state,
            },
            "summary": {
                "changed_fields": changed_count,
            },
            "field_changes": field_changes,
        }

    def get_comparison_payload(self):
        comparisons = [self.build_comparison_with(other) for other in self._get_other_versions()]
        return {
            "mode": "version_history",
            "title": f"Version Comparison: {self.name}",
            "subtitle": f"Version {self.version} compared with all versions of {self.product_id.name if self.product_id else 'this product'}",
            "subject": {
                "id": self.id,
                "name": self.name,
                "version": self.version,
                "state": self.state,
                "product_name": self.product_id.name if self.product_id else None,
            },
            "summary": {
                "comparisons": len(comparisons),
                "changed_fields": sum(item["summary"]["changed_fields"] for item in comparisons),
            },
            "comparisons": comparisons,
        }

    def action_open_comparison(self):
        return {
            "type": "ir.actions.client",
            "tag": "open_comparison_view",
            "params": {
                "model": self._model_name_,
                "record_id": self.id,
                "title": f"Compare {self.name}",
            }
        }

    def _get_db(self):
        from sqlalchemy.orm import object_session
        return object_session(self)

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

    def action_set_active(self):
        self.write({"state": "active"})
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Version Activated",
                "message": f"'{self.name}' is now Active.",
                "type": "success",
                "refresh": True
            }
        }

    def action_set_archived(self):
        self.write({"state": "archived"})
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Version Archived",
                "message": f"'{self.name}' has been Archived.",
                "type": "warning",
                "refresh": True
            }
        }

    def action_reset_draft(self):
        self.write({"state": "draft"})
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Reset to Draft",
                "message": f"'{self.name}' has been reset to Draft.",
                "type": "info",
                "refresh": True
            }
        }
