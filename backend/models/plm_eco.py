from datetime import datetime
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
    }, readonly="[('stage_is_last', '=', True)]")

    stage_id = fields.Many2one(
        "plm.eco.stage", label="Stage", tracking=True, readonly=True,
        help="Current stage of this ECO in the approval workflow."
    )
    able_to_move_to_next_stage = fields.Boolean(
        label="Able to Move to Next Stage",
        default=False,
        readonly=True,
        tracking=True,
        help="Becomes true once all required approvals for the current stage are complete."
    )

    description = fields.Text(label="Description", tracking=True, readonly="[('stage_is_last', '=', True)]")
    update_version = fields.Boolean(label="Update Version", default=True, tracking=True, readonly="[('stage_is_last', '=', True)]")
    initiated_by_id = fields.Many2one("user", label="Initiated By", default="current_user", tracking=True, readonly="[('stage_is_last', '=', True)]")
    approval_ids = fields.One2many(
        "plm.eco.approval", "eco_id",
        label="Approvals",
        columns=["stage_id", "user_id", "approval_required", "approved", "approval_time"],
        readonly=True,
        show_label=False,
    )

    # Shown in top form, hidden based on type
    product_id = fields.Many2one(
        "product.product", label="Product",
        invisible="[('type', '!=', 'product')]",
        required="[('type', '=', 'product')]",
        domain="[('current_version_id', '!=', False)]",
        tracking=True,
        readonly="[('stage_is_last', '=', True)]"
    )
    bom_id = fields.Many2one(
        "mrp.bom", label="Target BoM",
        invisible="[('type', '!=', 'bom')]",
        required="[('type', '=', 'bom')]",
        domain="[('state', '=', 'active')]",
        tracking=True,
        readonly="[('stage_is_last', '=', True)]"
    )

    # Product ECO change fields
    eco_name = fields.Char(label="Product Name", size=200, tracking=True,
                           invisible="[('type', '!=', 'product')]",
                           readonly="[('stage_is_last', '=', True)]")
    eco_default_code = fields.Char(label="Internal Reference", size=100, tracking=True,
                                   invisible="[('type', '!=', 'product')]",
                                   readonly="[('stage_is_last', '=', True)]")
    eco_sale_price = fields.Integer(label="Sale Price", default=0, tracking=True,
                                    invisible="[('type', '!=', 'product')]",
                                    readonly="[('stage_is_last', '=', True)]")
    eco_cost_price = fields.Integer(label="Cost Price", default=0, tracking=True,
                                    invisible="[('type', '!=', 'product')]",
                                    readonly="[('stage_is_last', '=', True)]")
    eco_change_notes = fields.Text(label="Change Notes", tracking=True,
                                   invisible="[('type', '!=', 'product')]",
                                   readonly="[('stage_is_last', '=', True)]")
    eco_attachments = fields.Attachments(
        label="Attachments",
        allowed_types=["pdf", "doc", "docx", "png", "jpg", "jpeg", "xlsx", "csv"],
        max_size=10485760,
        invisible="[('type', '!=', 'product')]",
        readonly="[('stage_is_last', '=', True)]"
    )

    # BoM ECO change fields
    eco_line_ids = fields.One2many(
        "plm.eco.line", "eco_id",
        label="Proposed Components",
        columns=["component_product_id", "quantity", "notes"],
        invisible="[('type', '!=', 'bom')]",
        readonly="[('stage_is_last', '=', True)]",
        show_label=False,
    )
    eco_workorder_ids = fields.One2many(
        "plm.eco.workorder", "eco_id",
        label="Proposed Work Orders",
        columns=["operation", "work_center_id", "duration_minutes"],
        invisible="[('type', '!=', 'bom')]",
        readonly="[('stage_is_last', '=', True)]",
        show_label=False,
    )
    old_product_count = fields.Integer(label="Old Product Version", compute="_compute_old_product_count", store=False)
    new_product_count = fields.Integer(label="New Product Version", compute="_compute_new_product_count", store=False)
    single_product_count = fields.Integer(label="Product Version", compute="_compute_single_product_count", store=False)
    old_bom_count = fields.Integer(label="Old BoM", compute="_compute_old_bom_count", store=False)
    new_bom_count = fields.Integer(label="New BoM", compute="_compute_new_bom_count", store=False)
    single_bom_count = fields.Integer(label="BoM", compute="_compute_single_bom_count", store=False)
    comparison_count = fields.Integer(label="Compare", compute="_compute_comparison_count", store=False)

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
                    "name": "approve_current_stage",
                    "label": "Approve",
                    "type": "primary",
                    "method": "action_approve_current_stage",
                    "invisible": "[('can_current_user_approve', '=', False)]"
                },
                {
                    "name": "refuse_current_stage",
                    "label": "Refuse",
                    "type": "danger",
                    "method": "action_refuse_current_stage",
                    "invisible": "[('can_current_user_refuse', '=', False)]"
                },
                {
                    "name": "move_to_next_stage",
                    "label": "Move to Next stage",
                    "type": "primary",
                    "method": "action_move_to_next_stage",
                    "invisible": "[('able_to_move_to_next_stage', '=', False)]"
                },
                {
                    "name": "move_to_draft",
                    "label": "Move to Draft",
                    "type": "warning",
                    "method": "action_move_to_draft",
                    "invisible": "[('stage_is_refused', '=', False)]"
                }
            ],
            "smart_buttons": [
                {
                    "name": "old_product",
                    "label": "Old Product",
                    "icon": "Package",
                    "field": "old_product_count",
                    "method": "action_view_old_product",
                    "invisible": "['|', '|', ('type', '!=', 'product'), ('update_version', '=', False), ('old_product_count', '=', 0)]"
                },
                {
                    "name": "new_product",
                    "label": "New Product",
                    "icon": "Package",
                    "field": "new_product_count",
                    "method": "action_view_new_product",
                    "invisible": "['|', '|', ('type', '!=', 'product'), ('update_version', '=', False), ('new_product_count', '=', 0)]"
                },
                {
                    "name": "single_product",
                    "label": "Product",
                    "icon": "Package",
                    "field": "single_product_count",
                    "method": "action_view_single_product",
                    "invisible": "['|', '|', ('type', '!=', 'product'), ('update_version', '=', True), ('single_product_count', '=', 0)]"
                },
                {
                    "name": "old_bom",
                    "label": "Old BoM",
                    "icon": "Layers",
                    "field": "old_bom_count",
                    "method": "action_view_old_bom",
                    "invisible": "['|', '|', ('type', '!=', 'bom'), ('update_version', '=', False), ('old_bom_count', '=', 0)]"
                },
                {
                    "name": "new_bom",
                    "label": "New BoM",
                    "icon": "Layers",
                    "field": "new_bom_count",
                    "method": "action_view_new_bom",
                    "invisible": "['|', '|', ('type', '!=', 'bom'), ('update_version', '=', False), ('new_bom_count', '=', 0)]"
                },
                {
                    "name": "single_bom",
                    "label": "BoM",
                    "icon": "Layers",
                    "field": "single_bom_count",
                    "method": "action_view_single_bom",
                    "invisible": "['|', '|', ('type', '!=', 'bom'), ('update_version', '=', True), ('single_bom_count', '=', 0)]"
                },
                {
                    "name": "comparison",
                    "label": "Compare",
                    "icon": "GitCompare",
                    "field": "comparison_count",
                    "method": "action_open_comparison",
                    "invisible": "[('comparison_count', '=', 0)]"
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
                            "title": "Change Notes",
                            "fields": ["eco_change_notes"]
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
                    "fields": ["eco_line_ids"]
                },
                {
                    "title": "Work Orders",
                    "invisible": "[('type', '!=', 'bom')]",
                    "fields": ["eco_workorder_ids"]
                },
                {
                    "title": "Approvals",
                    "fields": ["approval_ids"]
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
        if stage and hasattr(stage, 'is_refused_stage'):
            data['stage_is_refused'] = bool(stage.is_refused_stage)
        else:
            data['stage_is_refused'] = False
        data['able_to_move_to_next_stage'] = bool(self.able_to_move_to_next_stage)

        user_context = kwargs.get("user_context") or {}
        current_user_id = user_context.get("id")
        data['can_current_user_approve'] = self._can_user_approve_current_stage(current_user_id)
        data['can_current_user_refuse'] = self._can_user_refuse_current_stage(current_user_id)
        return data

    def _get_db(self):
        from sqlalchemy.orm import object_session
        return object_session(self)

    def _get_new_product_version(self, db=None):
        from backend.core.base_model import Environment

        if self.type != "product" or not self.product_id:
            return None

        db = db or self._get_db()
        if not db:
            return None

        env = Environment(db)
        version = env["product.version"].search([("eco_id", "=", self.id)], limit=1)
        if version:
            if isinstance(version, (list, tuple)):
                return version[0] if version else None
            return version

        return None

    def _get_old_product_version(self, db=None):
        from backend.core.base_model import Environment

        if self.type != "product" or not self.product_id:
            return None

        db = db or self._get_db()
        if not db:
            return None

        new_version = self._get_new_product_version(db)
        if not new_version:
            return self.product_id.current_version_id if self.update_version else None

        env = Environment(db)
        old_version = env["product.version"].search(
            [("product_id", "=", self.product_id.id), ("id", "!=", new_version.id)],
            order="version desc",
            limit=1
        )
        if old_version:
            if isinstance(old_version, (list, tuple)):
                return old_version[0] if old_version else None
            return old_version

        return None

    def _get_single_product_version(self, db=None):
        if self.type != "product" or self.update_version:
            return None

        return self.product_id.current_version_id if self.product_id else None

    def _get_new_bom(self, db=None):
        from backend.core.base_model import Environment

        if self.type != "bom" or not self.bom_id:
            return None

        db = db or self._get_db()
        if not db:
            return None

        env = Environment(db)
        bom = env["mrp.bom"].search([("eco_id", "=", self.id)], limit=1)
        if bom:
            if isinstance(bom, (list, tuple)):
                return bom[0] if bom else None
            return bom

        return None

    def _get_old_bom(self, db=None):
        if self.type != "bom" or not self.update_version:
            return None

        return self.bom_id

    def _get_single_bom(self, db=None):
        if self.type != "bom" or self.update_version:
            return None

        return self.bom_id

    def _get_comparison_targets(self, db=None):
        if self.type == "product":
            old_record = self._get_old_product_version(db)
            new_record = self._get_new_product_version(db)
        elif self.type == "bom":
            old_record = self._get_old_bom(db)
            new_record = self._get_new_bom(db)
        else:
            old_record = None
            new_record = None
        return old_record, new_record

    def _get_current_stage_approvals(self, db=None):
        from backend.core.base_model import Environment

        db = db or self._get_db()
        if not db or not self.id or not self.stage_id:
            return []

        env = Environment(db)
        approvals = env["plm.eco.approval"].search([
            ("eco_id", "=", self.id),
            ("stage_id", "=", self.stage_id.id),
        ], order="id")
        return list(approvals._records)

    @api.depends("type", "product_id", "update_version", "stage_id")
    def _compute_old_product_count(self):
        self.old_product_count = 1 if self._get_old_product_version() else 0

    @api.depends("type", "product_id", "update_version", "stage_id")
    def _compute_new_product_count(self):
        self.new_product_count = 1 if self._get_new_product_version() else 0

    @api.depends("type", "product_id", "update_version", "stage_id")
    def _compute_single_product_count(self):
        self.single_product_count = 1 if self._get_single_product_version() else 0

    @api.depends("type", "bom_id", "update_version", "stage_id")
    def _compute_old_bom_count(self):
        self.old_bom_count = 1 if self._get_old_bom() else 0

    @api.depends("type", "bom_id", "update_version", "stage_id")
    def _compute_new_bom_count(self):
        self.new_bom_count = 1 if self._get_new_bom() else 0

    @api.depends("type", "bom_id", "update_version", "stage_id")
    def _compute_single_bom_count(self):
        self.single_bom_count = 1 if self._get_single_bom() else 0

    @api.depends("type", "product_id", "bom_id", "update_version", "stage_id")
    def _compute_comparison_count(self):
        old_record, new_record = self._get_comparison_targets()
        self.comparison_count = 1 if old_record and new_record else 0

    def _can_user_approve_current_stage(self, user_id):
        if not user_id or not self.stage_id or not self.id:
            return False
        if getattr(self.stage_id, "is_refused_stage", False):
            return False

        for approval in self._get_current_stage_approvals():
            if (
                approval.approval_required
                and not approval.approved
                and approval.user_id
                and approval.user_id.id == user_id
            ):
                return True
        return False

    def _can_user_refuse_current_stage(self, user_id):
        return self._can_user_approve_current_stage(user_id)

    def action_view_old_product(self):
        version = self._get_old_product_version()
        if not version:
            return {}
        return {
            "type": "ir.actions.act_window",
            "res_model": "product.version",
            "view_mode": "form",
            "res_id": version.id,
            "name": f"Old Product Version for {self.name}"
        }

    def action_view_new_product(self):
        version = self._get_new_product_version()
        if not version:
            return {}
        return {
            "type": "ir.actions.act_window",
            "res_model": "product.version",
            "view_mode": "form",
            "res_id": version.id,
            "name": f"New Product Version for {self.name}"
        }

    def action_view_single_product(self):
        version = self._get_single_product_version()
        if not version:
            return {}
        return {
            "type": "ir.actions.act_window",
            "res_model": "product.version",
            "view_mode": "form",
            "res_id": version.id,
            "name": f"Product Version for {self.name}"
        }

    def action_view_old_bom(self):
        bom = self._get_old_bom()
        if not bom:
            return {}
        return {
            "type": "ir.actions.act_window",
            "res_model": "mrp.bom",
            "view_mode": "form",
            "res_id": bom.id,
            "name": f"Old BoM for {self.name}"
        }

    def action_view_new_bom(self):
        bom = self._get_new_bom()
        if not bom:
            return {}
        return {
            "type": "ir.actions.act_window",
            "res_model": "mrp.bom",
            "view_mode": "form",
            "res_id": bom.id,
            "name": f"New BoM for {self.name}"
        }

    def action_view_single_bom(self):
        bom = self._get_single_bom()
        if not bom:
            return {}
        return {
            "type": "ir.actions.act_window",
            "res_model": "mrp.bom",
            "view_mode": "form",
            "res_id": bom.id,
            "name": f"BoM for {self.name}"
        }

    def action_open_comparison(self):
        old_record, new_record = self._get_comparison_targets()
        if not old_record or not new_record:
            return {}
        return {
            "type": "ir.actions.client",
            "tag": "open_comparison_view",
            "params": {
                "model": self._model_name_,
                "record_id": self.id,
                "title": f"Compare {self.name}",
            }
        }

    def get_comparison_payload(self):
        old_record, new_record = self._get_comparison_targets()
        if not old_record or not new_record:
            return {
                "mode": "empty",
                "title": f"Comparison: {self.name}",
                "subtitle": "Comparison is available only after a new version/BoM is created.",
                "summary": {
                    "changed_fields": 0,
                    "component_changes": 0,
                    "workorder_changes": 0,
                },
                "comparisons": [],
            }

        if self.type == "product":
            comparison = new_record.build_comparison_with(old_record)
            return {
                "mode": "pair",
                "entity_type": "product",
                "title": f"Product Comparison: {self.name}",
                "subtitle": f"Old version {old_record.version} vs new version {new_record.version}",
                "old_record": {
                    "id": old_record.id,
                    "name": old_record.name,
                    "version": old_record.version,
                    "state": old_record.state,
                },
                "new_record": {
                    "id": new_record.id,
                    "name": new_record.name,
                    "version": new_record.version,
                    "state": new_record.state,
                },
                "summary": {
                    "changed_fields": comparison["summary"]["changed_fields"],
                    "component_changes": 0,
                    "workorder_changes": 0,
                },
                "field_changes": comparison["field_changes"],
                "component_changes": [],
                "workorder_changes": [],
            }

        comparison = new_record.build_comparison_with(old_record)
        return {
            "mode": "pair",
            "entity_type": "bom",
            "title": f"BoM Comparison: {self.name}",
            "subtitle": f"Old BoM {old_record.name} vs new BoM {new_record.name}",
            "old_record": comparison["old_record"],
            "new_record": comparison["new_record"],
            "summary": comparison["summary"],
            "field_changes": comparison["field_changes"],
            "component_changes": comparison["component_changes"],
            "workorder_changes": comparison["workorder_changes"],
        }

    def _ensure_stage_approval_tracking(self, db):
        if not db or not self.id or not self.stage_id:
            return

        existing_by_user = {
            approval.user_id.id: approval
            for approval in self._get_current_stage_approvals(db)
            if approval.user_id
        }

        for line in self.stage_id.approval_line_ids or []:
            if not line.user_id or line.user_id.id in existing_by_user:
                continue

            from backend.core.registry import registry
            approval_cls = registry.get_model("plm.eco.approval")
            approval = approval_cls(
                eco_id=self.id,
                stage_id=self.stage_id.id,
                user_id=line.user_id.id,
                approval_required=bool(line.approval_required),
                approved=False,
                approval_time=None,
            )
            db.add(approval)
            db.flush()

    def _update_stage_movement_state(self, db):
        stage = self.stage_id
        if not stage:
            self.able_to_move_to_next_stage = False
            db.flush()
            return

        approvals = self._get_current_stage_approvals(db)
        required_approvals = [approval for approval in approvals if approval.approval_required]

        self.able_to_move_to_next_stage = (
            not bool(stage.is_last_stage)
            and not bool(getattr(stage, "is_refused_stage", False))
            and all(approval.approved for approval in required_approvals)
        )
        db.flush()

    def _get_refused_stage(self, db):
        from backend.core.base_model import Environment

        env = Environment(db)
        stages = env["plm.eco.stage"].search([("is_refused_stage", "=", True)], limit=1)
        return stages[0] if stages else None

    @classmethod
    def _get_first_workflow_stage(cls, db):
        from backend.core.base_model import Environment

        env = Environment(db)
        stages = env["plm.eco.stage"].search([("is_refused_stage", "=", False)], order="sequence", limit=1)
        if stages:
            return stages[0]

        # Fallback for older stage rows where the new boolean may not be populated yet.
        stages = env["plm.eco.stage"].search([], order="sequence", limit=1)
        return stages[0] if stages else None

    def _reset_approval_state(self, db):
        if not db or not self.id:
            return

        from backend.core.base_model import Environment

        env = Environment(db)
        approvals = env["plm.eco.approval"].search([("eco_id", "=", self.id)])
        for approval in approvals:
            approval.approved = False
            approval.approval_time = None
        db.flush()

    def _sync_stage_approval_state(self, db):
        if not db:
            return
        self._ensure_stage_approval_tracking(db)
        self._update_stage_movement_state(db)
        db.refresh(self)

    def _archive_current_product_version(self, db):
        if self.type != "product" or not self.product_id or not self.update_version:
            return

        current_version = self.product_id.current_version_id
        if current_version and getattr(current_version, "state", None) != "archived":
            current_version.write(db, {"state": "archived"})

    def _archive_current_bom(self, db):
        if self.type != "bom" or not self.bom_id:
            return

        current_bom = self.bom_id
        if getattr(current_bom, "state", None) != "archived":
            current_bom.write(db, {"state": "archived"})

    def _sync_bom_lines_from_eco(self, db, bom):
        from backend.core.registry import registry
        from backend.core.base_model import Environment

        if not bom:
            return None

        env = Environment(db)
        bom_line_model = registry.get_model("mrp.bom.line")
        routing_model = registry.get_model("mrp.routing.workcenter")

        if bom_line_model:
            db.query(bom_line_model).filter(
                bom_line_model.__table__.c.bom_id == bom.id
            ).delete(synchronize_session=False)

        if routing_model:
            db.query(routing_model).filter(
                routing_model.__table__.c.bom_id == bom.id
            ).delete(synchronize_session=False)

        for line in self.eco_line_ids or []:
            component_version = line.component_product_id
            component_version_id = (
                component_version.id
                if component_version and hasattr(component_version, "id")
                else None
            )
            if not component_version_id:
                continue
            env["mrp.bom.line"].create({
                "bom_id": bom.id,
                "component_product_id": component_version_id,
                "quantity": line.quantity or 1,
                "notes": line.notes or "",
            })

        for workorder in self.eco_workorder_ids or []:
            work_center = workorder.work_center_id
            work_center_id = (
                work_center.id
                if work_center and hasattr(work_center, "id")
                else None
            )
            if not work_center_id:
                continue
            env["mrp.routing.workcenter"].create({
                "bom_id": bom.id,
                "operation": workorder.operation or "",
                "work_center_id": work_center_id,
                "duration_minutes": workorder.duration_minutes or 0,
            })

        db.flush()
        db.refresh(bom)
        return bom

    def _get_product_version_name(self):
        if self.type != "product":
            return self.name
        return (self.eco_name or (self.product_id.name if self.product_id else None) or self.name or "").strip()

    def _build_product_version_vals(self, db):
        return {
            "name": self._get_product_version_name(),
            "default_code": self.eco_default_code,
            "description": self.eco_change_notes,
            "sale_price": self.eco_sale_price or 0,
            "cost_price": self.eco_cost_price or 0,
            "eco_id": self.id,
            "state": "active",
            "attachments": self._get_eco_attachments(db),
        }

    def _sync_product_from_version(self, db, version):
        if not self.product_id or not version:
            return

        product_name = getattr(version, "name", None) or self._get_product_version_name()
        self.product_id.write(db, {
            "name": product_name,
            "current_version_id": version.id,
        })

    def _update_current_product_version_from_eco(self, db):
        if self.type != "product" or not self.product_id:
            return None

        current_version = self.product_id.current_version_id
        if not current_version:
            return None

        current_version.write(db, self._build_product_version_vals(db))
        self._sync_product_from_version(db, current_version)
        db.refresh(current_version)
        return current_version

    def _activate_product_version_from_eco(self, db):
        from backend.core.base_model import Environment

        if self.type != "product" or not self.product_id:
            return None
        if not self.update_version:
            return self._update_current_product_version_from_eco(db)

        env = Environment(db)
        existing_version = env["product.version"].search([("eco_id", "=", self.id)], limit=1)
        if existing_version:
            version = existing_version[0]
            version.write(db, self._build_product_version_vals(db))
            self._sync_product_from_version(db, version)
            db.refresh(version)
            return version

        latest_version = env["product.version"].search(
            [("product_id", "=", self.product_id.id)],
            order="version desc",
            limit=1
        )
        next_version_number = (latest_version[0].version + 1) if latest_version else 1
        version_vals = {
            "product_id": self.product_id.id,
            "version": next_version_number,
            **self._build_product_version_vals(db),
        }

        version = env["product.version"].create(version_vals)
        self._sync_product_from_version(db, version)
        db.refresh(version)
        return version

    def _activate_bom_from_eco(self, db):
        from backend.core.base_model import Environment

        if self.type != "bom" or not self.bom_id:
            return None

        env = Environment(db)
        source_bom = self.bom_id
        product_version = source_bom.product_version_id
        if not product_version:
            return None

        if not self.update_version:
            source_bom.write(db, {
                "notes": self.description or source_bom.notes,
                "eco_id": self.id,
            })
            return self._sync_bom_lines_from_eco(db, source_bom)

        existing_bom = env["mrp.bom"].search([("eco_id", "=", self.id)], limit=1)
        if existing_bom:
            if isinstance(existing_bom, (list, tuple)):
                existing_bom = existing_bom[0] if existing_bom else None
        if existing_bom:
            return self._sync_bom_lines_from_eco(db, existing_bom)

        self._archive_current_bom(db)

        new_bom = env["mrp.bom"].create({
            "name": "New",
            "product_version_id": product_version.id,
            "version": (source_bom.version or 0) + 1,
            "state": "active",
            "notes": self.description or source_bom.notes,
            "eco_id": self.id,
        })
        return self._sync_bom_lines_from_eco(db, new_bom)

    def _get_eco_attachments(self, db):
        from backend.core.registry import registry

        attachment_model = registry.get_model("ir.attachment")
        if not attachment_model or not self.id:
            return []

        attachments = db.query(attachment_model).filter(
            attachment_model.res_model == self._model_name_,
            attachment_model.res_id == self.id,
            attachment_model.res_field == "eco_attachments"
        ).all()
        attachment_payloads = []
        for attachment in attachments:
            attachment_payloads.append({
                "name": attachment.name,
                "datas": attachment.datas,
                "file_size": attachment.file_size,
                "mimetype": attachment.mimetype,
                "description": attachment.description,
            })
        return attachment_payloads

    def action_move_to_next_stage(self):
        """Move this ECO to the next stage ordered by sequence."""
        from backend.core.base_model import Environment
        db = self._get_db()
        if not db:
            return {"type": "error", "message": "No database session"}

        current_stage = self.stage_id
        if not current_stage:
            return {"type": "error", "message": "No current stage set"}
        if getattr(current_stage, "is_refused_stage", False):
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Refused Stage",
                    "message": "A refused ECO must be moved back to Draft before continuing.",
                    "type": "warning",
                }
            }

        self._sync_stage_approval_state(db)
        if not self.able_to_move_to_next_stage:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Approvals Pending",
                    "message": "All required approvals must be completed before moving to the next stage.",
                    "type": "warning",
                }
            }

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
        if next_stage.is_last_stage:
            if self.type == "product":
                self._activate_product_version_from_eco(db)
            elif self.type == "bom":
                self._activate_bom_from_eco(db)

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

    def action_refuse_current_stage(self):
        db = self._get_db()
        if not db:
            return {"type": "error", "message": "No database session"}
        if not self.stage_id:
            raise UserError("This ECO does not have a current stage.")
        if getattr(self.stage_id, "is_refused_stage", False):
            raise UserError("This ECO is already in the refused stage.")

        current_user_id = getattr(self, "_action_user_id", None) or getattr(self, "_audit_user_id", None)
        if not current_user_id:
            raise UserError("Could not determine the current user for refusal.")
        if not self._can_user_refuse_current_stage(current_user_id):
            raise UserError("You do not have any pending required approval for this ECO stage.")

        refused_stage = self._get_refused_stage(db)
        if not refused_stage:
            raise UserError("No refused stage is configured. Mark one ECO stage as the refused stage first.")

        self.write(db, {"stage_id": refused_stage.id})
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "ECO Refused",
                "message": f"ECO moved to stage: {refused_stage.name}",
                "type": "warning",
                "refresh": True,
            }
        }

    def action_move_to_draft(self):
        db = self._get_db()
        if not db:
            return {"type": "error", "message": "No database session"}
        if not self.stage_id or not getattr(self.stage_id, "is_refused_stage", False):
            raise UserError("Only ECOs in the refused stage can be moved back to draft.")

        draft_stage = self.__class__._get_first_workflow_stage(db)
        if not draft_stage:
            raise UserError("No draft stage is configured.")

        self._reset_approval_state(db)
        self.write(db, {"stage_id": draft_stage.id})
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Moved to Draft",
                "message": f"ECO moved to stage: {draft_stage.name}",
                "type": "info",
                "refresh": True,
            }
        }

    def action_approve_current_stage(self):
        db = self._get_db()
        if not db:
            return {"type": "error", "message": "No database session"}
        if not self.stage_id:
            raise UserError("This ECO does not have a current stage.")

        current_user_id = getattr(self, "_action_user_id", None) or getattr(self, "_audit_user_id", None)
        if not current_user_id:
            raise UserError("Could not determine the current user for approval.")

        approvals = [
            approval for approval in self._get_current_stage_approvals(db)
            if (
                approval.approval_required
                and not approval.approved
                and approval.user_id
                and approval.user_id.id == current_user_id
            )
        ]

        if not approvals:
            raise UserError("You do not have any pending required approval for this ECO stage.")

        approved_at = datetime.utcnow()
        for approval in approvals:
            approval.approved = True
            approval.approval_time = approved_at

        db.flush()
        self._sync_stage_approval_state(db)

        message = "Your approval has been recorded."
        if self.able_to_move_to_next_stage:
            message = "Your approval has been recorded. All required approvals are complete."

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Stage Approved",
                "message": message,
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
                    stage = cls._get_first_workflow_stage(db)
                    if stage:
                        res['stage_id'] = stage.id
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
        self.eco_change_notes = version.description or ""

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

        # ── bom_id changed: populate ECO component/work-order lines from BOM ───
        elif field_name == "bom_id":
            bom_id = vals.get("bom_id")
            if isinstance(bom_id, dict):
                bom_id = bom_id.get("id")
            print(f"[ECO trigger_onchange] bom_id resolved={bom_id}")
            if bom_id:
                try:
                    from backend.core.registry import registry
                    bom_line_model = registry.get_model("mrp.bom.line")
                    routing_model = registry.get_model("mrp.routing.workcenter")
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
                    if routing_model:
                        routings = db.query(routing_model).filter(
                            routing_model.__table__.c.bom_id == bom_id
                        ).all()
                        print(f"[ECO trigger_onchange] found {len(routings)} routing lines for bom_id={bom_id}")
                        eco_workorders = []
                        for routing in routings:
                            work_center = routing.work_center_id
                            if work_center and hasattr(work_center, "id"):
                                work_center_id = work_center.id
                                work_center_name = work_center.name
                            else:
                                work_center_id = routing._raw_id("work_center_id")
                                work_center_name = str(work_center_id) if work_center_id else None
                            eco_workorders.append({
                                "id": None,
                                "operation": routing.operation or "",
                                "work_center_id": {
                                    "id": work_center_id,
                                    "display_name": work_center_name or str(work_center_id),
                                } if work_center_id else None,
                                "duration_minutes": routing.duration_minutes or 0,
                            })
                        print(f"[ECO trigger_onchange] eco_workorders={eco_workorders}")
                        result["eco_workorder_ids"] = eco_workorders
                except Exception as e:
                    import logging
                    logging.getLogger(__name__).warning(
                        f"Could not load BOM lines/work orders in onchange: {e}"
                    )
                    print(f"[ECO trigger_onchange] BOM lines/work orders error: {e}")
            else:
                print(f"[ECO trigger_onchange] bom_id cleared, wiping eco_line_ids and eco_workorder_ids")
                result["eco_line_ids"] = []
                result["eco_workorder_ids"] = []

        print(
            f"[ECO trigger_onchange] final result keys={list(result.keys())}, "
            f"eco_line_ids={result.get('eco_line_ids')}, "
            f"eco_workorder_ids={result.get('eco_workorder_ids')}"
        )
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
        record = super().create(db, vals)
        record._archive_current_product_version(db)
        record._sync_stage_approval_state(db)
        db.commit()
        db.refresh(record)
        return record

    def write(self, *args, **kwargs):
        vals = args[1] if len(args) == 2 else (args[0] if args else kwargs)
        for f in ("product_id", "bom_id"):
            if isinstance(vals.get(f), dict):
                vals[f] = vals[f].get("id")
        if isinstance(vals.get("stage_id"), dict):
            vals["stage_id"] = vals["stage_id"].get("id")
        # Merge with current values to validate the final state
        merged = {
            "type":       vals.get("type", self.type),
            "product_id": vals.get("product_id", self.product_id.id if self.product_id else None),
            "bom_id":     vals.get("bom_id", self.bom_id.id if self.bom_id else None),
        }
        self._validate_type_required(merged)
        stage_changed = "stage_id" in vals
        result = super().write(*args, **kwargs)

        db = args[0] if len(args) == 2 else self._get_db()
        if db and (stage_changed or "able_to_move_to_next_stage" not in vals):
            self._sync_stage_approval_state(db)
            db.commit()
            db.refresh(self)

        return result
