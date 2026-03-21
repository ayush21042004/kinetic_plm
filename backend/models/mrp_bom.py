from backend.core.znova_model import ZnovaModel
from backend.core import fields, api
from backend.core.exceptions import UserError
from sqlalchemy.orm import Session


class Bom(ZnovaModel):
    __tablename__ = "mrp_bom"
    _model_name_ = "mrp.bom"
    _name_field_ = "reference"
    _description_ = "Bill of Materials"

    reference = fields.Char(label="Reference", required=True, size=100, tracking=True,
                            help="e.g. BOM-001, BoM-v2")

    product_version_id = fields.Many2one(
        "product.version", label="Product", required=True, tracking=True
    )
    version = fields.Integer(label="BoM Version", required=True, default=1, tracking=True, readonly=True)

    state = fields.Selection([
        ("draft",    "Draft"),
        ("active",   "Active"),
        ("archived", "Archived"),
    ], label="State", default="draft", tracking=True, options={
        "draft":    {"label": "Draft",    "color": "info"},
        "active":   {"label": "Active",   "color": "success"},
        "archived": {"label": "Archived", "color": "secondary"},
    })

    notes = fields.Text(label="Notes")
    eco_id = fields.Many2one("plm.eco", label="Source ECO", readonly=True)

    bom_line_ids = fields.One2many(
        "mrp.bom.line", "bom_id",
        label="Components",
        columns=["component_product_id", "quantity", "notes"]
    )
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
            {"name": "by_version", "label": "By Product Version", "field": "product_version_id"},
            {"name": "by_state",   "label": "By State",           "field": "state"},
        ]
    }

    _ui_views = {
        "list": {
            "fields": ["reference", "product_version_id", "version", "state"],
            "search_fields": ["reference", "product_version_id"]
        },
        "form": {
            "show_audit_log": True,
            "smart_buttons": [
                {
                    "name": "eco",
                    "label": "Source ECO",
                    "icon": "GitBranch",
                    "field": "eco_count",
                    "method": "action_view_eco",
                    "invisible": "[('eco_id', '=', false)]"
                }
            ],
            "groups": [
                {"title": "Reference", "fields": ["reference"], "position": "header"},
                {"title": "BoM Identity", "fields": ["product_version_id", "version"]},
            ],
            "tabs": [
                {
                    "title": "Components",
                    "fields": ["bom_line_ids"]
                },
                {
                    "title": "Notes",
                    "groups": [
                        {
                            "title": "Notes",
                            "fields": ["notes"]
                        }
                    ]
                }
            ]
        }
    }

    @api.depends("eco_id")
    def _compute_eco_count(self):
        self.eco_count = 1 if self.eco_id else 0

    def action_view_eco(self):
        if not self.eco_id:
            return {}
        return {
            "type": "ir.actions.act_window",
            "res_model": "plm.eco",
            "view_mode": "form",
            "res_id": self.eco_id.id,
            "name": f"ECO for {self.reference}"
        }

    @classmethod
    def create(cls, db, vals: dict):
        """Validate that no component's product version matches the BOM's product version."""
        env = cls.get_env(db)

        bom_version_id = vals.get("product_version_id")
        lines = vals.get("bom_line_ids", [])

        print(f"[BOM.create] bom_version_id={bom_version_id}, raw lines={lines}")

        cls._validate_no_self_reference(env, bom_version_id, lines)

        bom = super().create(db, vals)

        # Link the product version's bom_id back to this BOM
        if bom_version_id:
            version = env["product.version"].search(
                [("id", "=", bom_version_id)], limit=1
            )
            if version:
                version.write({"bom_id": bom.id})

        return bom
    def write(self, *args, **kwargs):
        """Also validate on update."""
        db = None
        vals = {}
        if len(args) == 2 and isinstance(args[0], Session):
            db, vals = args
        elif len(args) == 1:
            vals = args[0]
        else:
            vals = kwargs

        if db is None:
            from sqlalchemy.orm import object_session
            db = object_session(self)

        env = self.__class__.get_env(db)
        bom_version_id = vals.get("product_version_id")
        if bom_version_id is None and self.product_version_id:
            bom_version_id = self.product_version_id.id
        # Many2one can arrive as a dict
        if isinstance(bom_version_id, dict):
            bom_version_id = bom_version_id.get("id")
        lines = vals.get("bom_line_ids", [])

        print(f"[BOM.write] id={self.id}, bom_version_id={bom_version_id}, raw lines={lines}")

        self._validate_no_self_reference(env, bom_version_id, lines, exclude_id=self.id)

        result = super().write(*args, **kwargs)

        # If product_version_id was updated, unlink old version and link new one
        new_version_id = vals.get("product_version_id")
        if new_version_id:
            if isinstance(new_version_id, dict):
                new_version_id = new_version_id.get("id")
            if new_version_id:
                # Clear bom_id on the old version (if it was pointing to this BOM)
                old_version = env["product.version"].search(
                    [("bom_id", "=", self.id)], limit=1
                )
                if old_version and old_version.id != new_version_id:
                    old_version.write({"bom_id": None})

                # Link the new version
                new_version = env["product.version"].search(
                    [("id", "=", new_version_id)], limit=1
                )
                if new_version:
                    new_version.write({"bom_id": self.id})

        return result

    @classmethod
    def _validate_no_self_reference(cls, env, bom_version_id, lines, exclude_id=None):
        """
        1. A product version can only have one BOM.
        2. No component product can share the same version as the BOM target.
        """
        if not bom_version_id:
            return

        # ── Check 1: one BOM per product version ──────────────────────────────
        existing_bom = env["mrp.bom"].search(
            [("product_version_id", "=", bom_version_id)], limit=1
        )
        if existing_bom:
            # On write, ignore the current record itself
            if not exclude_id or existing_bom.id != exclude_id:
                raise UserError(
                    f"A BoM already exists for this product version. "
                    f"Each product version can only have one Bill of Materials."
                )

        # ── Check 2: no component = BOM target version ─────────────────────────
        if not lines:
            return

        # Normalise to flat list of line val dicts
        line_dicts = []
        if isinstance(lines, dict):
            for op, items in lines.items():
                if op in ("create", "update") and isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict):
                            line_dicts.append(item)
        elif isinstance(lines, list):
            for line in lines:
                if isinstance(line, (list, tuple)) and len(line) == 3:
                    if isinstance(line[2], dict):
                        line_dicts.append(line[2])
                elif isinstance(line, dict):
                    line_dicts.append(line)

        print(f"[BOM._validate] bom_version_id={bom_version_id}, normalised line_dicts={line_dicts}")

        for line_vals in line_dicts:
            component_version_id = line_vals.get("component_product_id")
            if not component_version_id:
                continue

            if isinstance(component_version_id, dict):
                component_version_id = component_version_id.get("id")
            if not component_version_id:
                continue

            # component is now a product.version — directly compare its id to the BOM version
            if component_version_id == bom_version_id:
                version = env["product.version"].search(
                    [("id", "=", component_version_id)], limit=1
                )
                label = version.name if version else f"#{component_version_id}"
                raise UserError(
                    f"Invalid BoM: component version '{label}' is the same as the BoM target version. "
                    f"A product version cannot be a component of itself."
                )
