from backend.core.znova_model import ZnovaModel
from backend.core import fields, api
from backend.core.exceptions import UserError


class Eco(ZnovaModel):
    __tablename__ = "plm_eco"
    _model_name_ = "plm.eco"
    _name_field_ = "name"
    _description_ = "Engineering Change Order"
    _status_field_ = "stage_id"

    _sequence_field = "name"
    _sequence_code = "plm.eco"

    name = fields.Char(label="ECO Reference", required=True, size=100, tracking=True,
                       help="e.g. ECO-00001", default="New", readonly=True)

    type = fields.Selection([
        ("product", "Product"),
        ("bom",     "BoM"),
    ], label="ECO Type", required=True, default="product", tracking=True, options={
        "product": {"label": "Product", "color": "primary"},
        "bom":     {"label": "BoM",     "color": "info"},
    })

    stage_id = fields.Many2one(
        "plm.eco.stage", label="Stage", tracking=True, readonly=True,
        help="Current stage of this ECO in the approval workflow."
    )

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
            {"name": "product_eco", "label": "Product ECOs", "domain": "[('type', '=', 'product')]"},
            {"name": "bom_eco",     "label": "BoM ECOs",     "domain": "[('type', '=', 'bom')]"},
        ],
        "group_by": [
            {"name": "by_type",  "label": "By Type",      "field": "type"},
            {"name": "by_stage", "label": "By Stage",     "field": "stage_id"},
            {"name": "by_user",  "label": "By Initiator", "field": "initiated_by_id"},
        ]
    }

    _ui_views = {
        "list": {
            "fields": ["name", "type", "stage_id", "product_id", "bom_id", "initiated_by_id"],
            "search_fields": ["name", "type", "stage_id"]
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
            "header_buttons": [
                {
                    "name": "move_to_next_stage",
                    "label": "Move to Next stage",
                    "type": "primary",
                    "method": "action_move_to_next_stage",
                    "invisible": "[('stage_is_last', '=', True)]"
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

    def to_dict(self, **kwargs):
        data = super().to_dict(**kwargs)
        # Inject flat boolean so the frontend domain [('stage_is_last', '=', True)] works
        stage = self.stage_id
        if stage and hasattr(stage, 'is_last_stage'):
            data['stage_is_last'] = bool(stage.is_last_stage)
        else:
            data['stage_is_last'] = False
        return data

    def action_move_to_next_stage(self):
        """Move this ECO to the next stage ordered by sequence."""
        from sqlalchemy.orm import object_session
        from backend.core.base_model import Environment
        db = object_session(self)
        if not db:
            return {"type": "error", "message": "No database session"}

        current_stage = self.stage_id
        if not current_stage:
            return {"type": "error", "message": "No current stage set"}

        current_seq = current_stage.sequence if hasattr(current_stage, "sequence") else 0

        env = Environment(db)
        # Find the next stage: lowest sequence that is greater than current
        all_stages = env["plm.eco.stage"].search(
            [("sequence", ">", current_seq)], order="sequence", limit=1
        )
        if not all_stages:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Already at Last Stage",
                    "message": "There is no next stage to move to.",
                    "type": "warning",
                }
            }

        next_stage = all_stages[0]
        self.write(db, {"stage_id": next_stage.id})
        db.commit()

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Stage Updated",
                "message": f"ECO moved to stage: {next_stage.name}",
                "type": "success",
                "refresh": True,
            }
        }

    @classmethod
    def default_get(cls, fields_list):
        res = super().default_get(fields_list)
        if 'stage_id' in fields_list and not res.get('stage_id'):
            try:
                from backend.core.base_model import Environment
                from backend.core.database import SessionLocal
                db = SessionLocal()
                try:
                    env = Environment(db)
                    stage = env['plm.eco.stage'].search([], order='sequence', limit=1)
                    if stage:
                        res['stage_id'] = stage[0].id
                finally:
                    db.close()
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Could not set default stage_id: {e}")
        return res

    @api.onchange("product_id")
    def _onchange_product_id(self):
        """When product changes, populate eco fields from the product's current version."""
        if not self.product_id:
            return

        product = getattr(self, 'product', None)
        if not product:
            print(f"[ECO onchange product_id] no product object loaded")
            return

        version = getattr(product, 'current_version', None)
        if not version:
            print(f"[ECO onchange product_id] product {product.id} has no current_version")
            return

        print(f"[ECO onchange product_id] filling from version id={version.id} name={version.name}")
        self.eco_name = version.name or ""
        self.eco_default_code = version.default_code or ""
        self.eco_sale_price = version.sale_price or 0
        self.eco_cost_price = version.cost_price or 0

    @api.onchange("bom_id")
    def _onchange_bom_id(self):
        """Marker method so the framework sets onchange=True on bom_id in UI metadata.
        Actual line population is handled in trigger_onchange override."""
        print(f"[ECO onchange bom_id] triggered, bom_id={self.bom_id}")

    @classmethod
    def trigger_onchange(cls, vals: dict, field_name: str, db=None):
        """
        Override to handle attachment population for product_id onchange,
        and BOM line population for bom_id onchange.
        """
        print(f"[ECO trigger_onchange] field_name={field_name}, vals={vals}")
        result = super().trigger_onchange(vals, field_name, db=db)
        print(f"[ECO trigger_onchange] base result keys={list(result.keys())}")

        if not db:
            print(f"[ECO trigger_onchange] no db session, returning base result")
            return result

        # ── product_id changed: inject version attachments ─────────────────────
        if field_name == "product_id":
            product_id = vals.get("product_id")
            if isinstance(product_id, dict):
                product_id = product_id.get("id")
            print(f"[ECO trigger_onchange] product_id resolved={product_id}")
            if product_id:
                try:
                    from backend.core.registry import registry
                    product_model = registry.get_model("product.product")
                    attachment_model = registry.get_model("ir.attachment")
                    if product_model and attachment_model:
                        product = db.get(product_model, product_id)
                        print(f"[ECO trigger_onchange] product={product}, current_version_id={getattr(product, 'current_version_id', None) if product else None}")
                        if product and product.current_version_id:
                            version_id = (
                                product.current_version_id.id
                                if hasattr(product.current_version_id, "id")
                                else product.current_version_id
                            )
                            attachments = db.query(attachment_model).filter(
                                attachment_model.res_model == "product.version",
                                attachment_model.res_id == version_id,
                                attachment_model.res_field == "attachments"
                            ).all()
                            print(f"[ECO trigger_onchange] found {len(attachments)} attachments for version {version_id}")
                            result["eco_attachments"] = [
                                att.to_dict(max_depth=0) for att in attachments
                            ]
                except Exception as e:
                    import logging
                    logging.getLogger(__name__).warning(
                        f"Could not load version attachments in onchange: {e}"
                    )
                    print(f"[ECO trigger_onchange] attachment error: {e}")

        # ── bom_id changed: populate eco_line_ids from BOM lines ───────────────
        elif field_name == "bom_id":
            bom_id = vals.get("bom_id")
            if isinstance(bom_id, dict):
                bom_id = bom_id.get("id")
            print(f"[ECO trigger_onchange] bom_id resolved={bom_id}")
            if bom_id:
                try:
                    from backend.core.registry import registry
                    bom_line_model = registry.get_model("mrp.bom.line")
                    print(f"[ECO trigger_onchange] bom_line_model={bom_line_model}")
                    if bom_line_model:
                        lines = db.query(bom_line_model).filter(
                            bom_line_model.__table__.c.bom_id == bom_id
                        ).all()
                        print(f"[ECO trigger_onchange] found {len(lines)} BOM lines for bom_id={bom_id}")
                        eco_lines = []
                        for line in lines:
                            comp_obj = line.component_product_id
                            print(f"[ECO trigger_onchange] line id={line.id}, comp_obj={comp_obj}, type={type(comp_obj)}")
                            if comp_obj and hasattr(comp_obj, 'id'):
                                comp_id = comp_obj.id
                                comp_name = comp_obj.name
                            else:
                                comp_id = line._raw_id('component_product_id')
                                comp_name = str(comp_id) if comp_id else None
                            print(f"[ECO trigger_onchange] comp_id={comp_id}, comp_name={comp_name}")
                            eco_lines.append({
                                "id": None,
                                "component_product_id": {
                                    "id": comp_id,
                                    "display_name": comp_name or str(comp_id),
                                } if comp_id else None,
                                "quantity": line.quantity,
                                "notes": line.notes or "",
                            })
                        print(f"[ECO trigger_onchange] eco_lines={eco_lines}")
                        result["eco_line_ids"] = eco_lines
                except Exception as e:
                    import logging
                    logging.getLogger(__name__).warning(
                        f"Could not load BOM lines in onchange: {e}"
                    )
                    print(f"[ECO trigger_onchange] BOM lines error: {e}")
            else:
                print(f"[ECO trigger_onchange] bom_id cleared, wiping eco_line_ids")
                result["eco_line_ids"] = []

        print(f"[ECO trigger_onchange] final result keys={list(result.keys())}, eco_line_ids={result.get('eco_line_ids')}")
        return result

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
        # Generate sequence if name is New/empty
        if vals.get("name") in (None, "", "New", "/"):
            from backend.models.sequence import Sequence
            vals["name"] = Sequence.next_by_code(db, cls._sequence_code)

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
