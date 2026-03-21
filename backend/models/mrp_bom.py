from backend.core.znova_model import ZnovaModel
from backend.core import fields, api
from backend.core.exceptions import UserError
from sqlalchemy.orm import Session


class Bom(ZnovaModel):
    __tablename__ = "mrp_bom"
    _model_name_ = "mrp.bom"
    _name_field_ = "name"
    _description_ = "Bill of Materials"

    _sequence_field = "name"
    _sequence_code = "mrp.bom"

    name = fields.Char(label="Reference", required=True, size=100, tracking=True,
                       help="e.g. BOM-00001", default="New", readonly=True)

    product_version_id = fields.Many2one(
        "product.version", label="Product", required=True, tracking=True,
        readonly="[('state', 'in', ['active', 'archived'])]"
    )
    version = fields.Integer(label="BoM Version", required=True, default=1, tracking=True, readonly=True)

    state = fields.Selection([
        ("draft",    "Draft"),
        ("active",   "Active"),
        ("archived", "Archived"),
    ], label="State", default="draft", tracking=True, readonly=True, options={
        "draft":    {"label": "Draft",    "color": "info"},
        "active":   {"label": "Active",   "color": "success"},
        "archived": {"label": "Archived", "color": "secondary"},
    })

    notes = fields.Text(label="Notes", readonly="[('state', 'in', ['active', 'archived'])]")
    eco_id = fields.Many2one("plm.eco", label="Source ECO", readonly=True, use_alter=True)

    bom_line_ids = fields.One2many(
        "mrp.bom.line", "bom_id",
        label="Components",
        columns=["component_product_id", "quantity", "notes"],
        readonly="[('state', 'in', ['active', 'archived'])]",
        show_label=False,
    )
    routing_workcenter_ids = fields.One2many(
        "mrp.routing.workcenter", "bom_id",
        label="Operations",
        columns=["operation", "work_center_id", "duration_minutes"],
        readonly="[('state', 'in', ['active', 'archived'])]",
        show_label=False,
    )
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
            {"name": "by_version", "label": "By Product Version", "field": "product_version_id"},
            {"name": "by_state",   "label": "By State",           "field": "state"},
        ]
    }

    _ui_views = {
        "list": {
            "fields": ["name", "product_version_id", "version", "state"],
            "search_fields": ["name", "product_version_id"]
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
                    "name": "eco",
                    "label": "Source ECO",
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
                {"title": "Reference", "fields": ["name"], "position": "header"},
                {"title": "BoM Identity", "fields": ["product_version_id", "version"]},
            ],
            "tabs": [
                {
                    "title": "Components",
                    "fields": ["bom_line_ids"]
                },
                {
                    "title": "Work Orders",
                    "fields": ["routing_workcenter_ids"]
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

    @api.depends("product_version_id")
    def _compute_comparison_count(self):
        self.comparison_count = len(self._get_other_versions())

    def action_set_active(self):
        self.write({"state": "active"})
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "BoM Activated",
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
                "title": "BoM Archived",
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

    def _get_db(self):
        from sqlalchemy.orm import object_session
        return object_session(self)

    def _get_other_versions(self):
        from backend.core.base_model import Environment

        db = self._get_db()
        if not db or not self.product_version_id or not self.product_version_id.product_id:
            return []

        env = Environment(db)
        version_records = env["product.version"].search(
            [("product_id", "=", self.product_version_id.product_id.id)],
            order="version desc"
        )
        version_ids = [version.id for version in list(getattr(version_records, "_records", version_records or []))]
        if not version_ids:
            return []

        boms = env["mrp.bom"].search(
            [("product_version_id", "in", version_ids), ("id", "!=", self.id)],
            order="version desc"
        )
        return list(getattr(boms, "_records", boms or []))

    def get_comparison_payload(self):
        comparisons = [self.build_comparison_with(other) for other in self._get_other_versions()]
        product_name = None
        if self.product_version_id and self.product_version_id.product_id:
            product_name = self.product_version_id.product_id.name

        return {
            "mode": "version_history",
            "entity_type": "bom",
            "title": f"BoM Comparison: {self.name}",
            "subtitle": f"BoM version {self.version} compared with all BoMs of {product_name or 'this product'}",
            "subject": {
                "id": self.id,
                "name": self.name,
                "version": self.version,
                "state": self.state,
                "product_name": product_name,
            },
            "summary": {
                "comparisons": len(comparisons),
                "changed_fields": sum(item["summary"]["changed_fields"] for item in comparisons),
                "component_changes": sum(item["summary"]["component_changes"] for item in comparisons),
                "workorder_changes": sum(item["summary"]["workorder_changes"] for item in comparisons),
            },
            "comparisons": [
                {
                    "target": item["old_record"],
                    "summary": item["summary"],
                    "field_changes": item["field_changes"],
                    "component_changes": item["component_changes"],
                    "workorder_changes": item["workorder_changes"],
                }
                for item in comparisons
            ],
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

    def _serialize_comparison_value(self, value):
        if value is None:
            return "-"
        if isinstance(value, dict):
            return " | ".join(f"{k}: {v}" for k, v in value.items()) if value else "-"
        return value

    def _get_item_diff(self, old_item, new_item, field_labels):
        """Identifies only changed fields and applies human-readable labels."""
        old_diff = {}
        new_diff = {}
        
        # Always include the identity label for added/removed items if available
        if not old_item and new_item and "label" in new_item:
            new_diff["Entity"] = new_item["label"]
        elif old_item and not new_item and "label" in old_item:
            old_diff["Entity"] = old_item["label"]

        for key, label in field_labels.items():
            ov = old_item.get(key) if old_item else None
            nv = new_item.get(key) if new_item else None
            
            # Treat None and empty string as equivalent to avoid "Notes: -" noise
            if not ov and not nv:
                continue
                
            if ov != nv:
                old_diff[label] = ov if ov is not None else "-"
                new_diff[label] = nv if nv is not None else "-"
        return old_diff, new_diff

    def _build_component_map(self):
        component_map = {}
        for line in self.bom_line_ids or []:
            component = line.component_product_id
            key = component.id if component else f"line-{line.id}"
            component_map[key] = {
                "label": component.name if component else f"Component #{key}",
                "quantity": line.quantity or 0,
                "notes": line.notes or "",
            }
        return component_map

    def _build_workorder_map(self):
        workorder_map = {}
        for line in self.routing_workcenter_ids or []:
            work_center = line.work_center_id
            key = f"{line.operation}::{work_center.id if work_center else 'none'}"
            workorder_map[key] = {
                "label": line.operation or "Work Order",
                "work_center": work_center.name if work_center else "-",
                "duration_minutes": line.duration_minutes or 0,
            }
        return workorder_map

    def build_comparison_with(self, other_bom):
        field_changes = []
        for field_name, label in {
            "notes": "Notes",
        }.items():
            old_value = getattr(other_bom, field_name, None)
            new_value = getattr(self, field_name, None)
            if old_value != new_value:
                field_changes.append({
                    "field": field_name,
                    "label": label,
                    "old_value": self._serialize_comparison_value(old_value),
                    "new_value": self._serialize_comparison_value(new_value),
                    "change_type": "updated",
                })

        component_labels = {"quantity": "Quantity", "notes": "Notes"}
        old_components = other_bom._build_component_map()
        new_components = self._build_component_map()
        component_changes = []
        for key in sorted(set(old_components.keys()) | set(new_components.keys())):
            old_item = old_components.get(key)
            new_item = new_components.get(key)
            
            if old_item and not new_item:
                # Removed: Show all fields with labels
                old_v, _ = self._get_item_diff(old_item, None, component_labels)
                component_changes.append({
                    "label": old_item["label"],
                    "change_type": "removed",
                    "old_value": self._serialize_comparison_value(old_v),
                    "new_value": None,
                })
            elif new_item and not old_item:
                # Added: Show all fields with labels
                _, new_v = self._get_item_diff(None, new_item, component_labels)
                component_changes.append({
                    "label": new_item["label"],
                    "change_type": "added",
                    "old_value": None,
                    "new_value": self._serialize_comparison_value(new_v),
                })
            elif old_item != new_item:
                # Updated: Show only changed fields
                old_v, new_v = self._get_item_diff(old_item, new_item, component_labels)
                component_changes.append({
                    "label": new_item["label"],
                    "change_type": "updated",
                    "old_value": self._serialize_comparison_value(old_v),
                    "new_value": self._serialize_comparison_value(new_v),
                })

        workorder_labels = {"work_center": "Work Center", "duration_minutes": "Duration (min)"}
        old_workorders = other_bom._build_workorder_map()
        new_workorders = self._build_workorder_map()
        workorder_changes = []
        for key in sorted(set(old_workorders.keys()) | set(new_workorders.keys())):
            old_item = old_workorders.get(key)
            new_item = new_workorders.get(key)
            
            if old_item and not new_item:
                old_v, _ = self._get_item_diff(old_item, None, workorder_labels)
                workorder_changes.append({
                    "label": old_item["label"],
                    "change_type": "removed",
                    "old_value": self._serialize_comparison_value(old_v),
                    "new_value": None,
                })
            elif new_item and not old_item:
                _, new_v = self._get_item_diff(None, new_item, workorder_labels)
                workorder_changes.append({
                    "label": new_item["label"],
                    "change_type": "added",
                    "old_value": None,
                    "new_value": self._serialize_comparison_value(new_v),
                })
            elif old_item != new_item:
                old_v, new_v = self._get_item_diff(old_item, new_item, workorder_labels)
                workorder_changes.append({
                    "label": new_item["label"],
                    "change_type": "updated",
                    "old_value": self._serialize_comparison_value(old_v),
                    "new_value": self._serialize_comparison_value(new_v),
                })

        return {
            "old_record": {"id": other_bom.id, "name": other_bom.name, "version": other_bom.version, "state": other_bom.state},
            "new_record": {"id": self.id, "name": self.name, "version": self.version, "state": self.state},
            "summary": {
                "changed_fields": len(field_changes),
                "component_changes": len(component_changes),
                "workorder_changes": len(workorder_changes),
            },
            "field_changes": field_changes,
            "component_changes": component_changes,
            "workorder_changes": workorder_changes,
        }

    @classmethod
    def create(cls, db, vals: dict):
        """Auto-generate sequence for name, validate no self-reference in components."""
        # Generate sequence if name is New/empty
        if vals.get("name") in (None, "", "New", "/"):
            from backend.models.sequence import Sequence
            vals["name"] = Sequence.next_by_code(db, cls._sequence_code)

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
        1. A product version can only have one non-archived BOM.
        2. No component product can share the same version as the BOM target.
        """
        if not bom_version_id:
            return

        # ── Check 1: one non-archived BOM per product version ─────────────────
        existing_bom = env["mrp.bom"].search(
            [("product_version_id", "=", bom_version_id), ("state", "!=", "archived")], limit=1
        )
        if existing_bom:
            # On write, ignore the current record itself
            if not exclude_id or existing_bom.id != exclude_id:
                raise UserError(
                    f"A BoM already exists for this product version. "
                    f"Each product version can only have one non-archived Bill of Materials."
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
