# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from inspect import getmembers

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class MixinTransactionReady(models.AbstractModel):
    _name = "mixin.transaction_ready"
    _inherit = [
        "mixin.transaction",
    ]
    _description = "Transaction Mixin - Ready to Start State Mixin"
    _ready_state = "ready"

    # Attributes related to add element on form view automatically
    _automatically_insert_ready_policy_fields = True
    _automatically_insert_ready_button = True

    # Attributes related to add element on search view automatically
    _automatically_insert_ready_filter = True

    # Attributes related to add element on tree view automatically
    _automatically_insert_ready_state_badge_decorator = True

    def _compute_policy(self):
        _super = super()
        _super._compute_policy()

    ready_ok = fields.Boolean(
        string="Can Stagged",
        compute="_compute_policy",
        compute_sudo=True,
        help="""Ready policy

* If active user can see and execute 'Staged' button""",
    )
    state = fields.Selection(
        selection_add=[
            ("ready", "Ready to Start"),
        ],
        ondelete={
            "ready": "set default",
        },
    )

    def _prepare_ready_data(self):
        self.ensure_one()
        result = {
            "state": self._ready_state,
        }
        if self._create_sequence_state == self._ready_state:
            self._create_sequence()
        return result

    def _run_pre_ready_check(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_pre_ready_check"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_post_ready_check(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_post_ready_check"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_pre_ready_action(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_pre_ready_action"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_post_ready_action(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_post_ready_action"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def action_ready(self):
        for record in self.sudo():
            record._check_ready_policy()
            record._run_pre_ready_check()
            record._run_pre_ready_action()
            record.write(record._prepare_ready_data())
            record._run_post_ready_check()
            record._run_post_ready_action()
            record._notify_ready_action()

    def _notify_ready_action(self):
        self.ensure_one()
        msg = self._prepare_ready_action_notification()
        self.message_post(
            body=_(msg), message_type="notification", subtype_xmlid="mail.mt_note"
        )

    def _prepare_ready_action_notification(self):
        self.ensure_one()
        msg = f"{self._description} {self.display_name} staged"
        return msg

    def _check_ready_policy(self):
        self.ensure_one()

        if not self._automatically_insert_ready_button:
            return True

        if self.env.context.get("bypass_policy_check", False):
            return True

        if not self.ready_ok:
            error_message = f"""
            Document Type: {self._description.lower()}
            Context: Stage document
            Database ID: {self.id}
            Problem: Document is not allowed to stage
            Solution: Check stage policy prerequisite
            """
            raise UserError(_(error_message))

    @api.model
    def _get_view(self, view_id=None, view_type="form", **options):
        view_arch, view = super()._get_view(
            view_id=view_id, view_type=view_type, **options
        )

        if view_type == "form" and self._automatically_insert_view_element:
            view_arch = self._view_add_ready_policy_field(view_arch)
            view_arch = self._view_add_ready_button(view_arch)
            view_arch = self._reorder_header_button(view_arch)
            view_arch = self._reorder_policy_field(view_arch)
        elif view_type == "list" and self._automatically_insert_view_element:
            view_arch = self._add_ready_state_badge_decorator(view_arch)
        elif view_type == "search" and self._automatically_insert_view_element:
            view_arch = self._add_ready_filter_on_search_view(view_arch)
            view_arch = self._reorder_state_filter_on_search_view(view_arch)

        return view_arch, view

    @api.model
    def _add_ready_state_badge_decorator(self, view_arch):
        if self._automatically_insert_ready_state_badge_decorator:
            _xpath = "/list/field[@name='state']"
            if len(view_arch.xpath(_xpath)) == 0:
                return view_arch
            node_xpath = view_arch.xpath(_xpath)[0]
            node_xpath.set("decoration-primary", "state == 'ready'")
        return view_arch

    @api.model
    def _add_ready_filter_on_search_view(self, view_arch):
        if self._automatically_insert_ready_filter:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_ready_mixin.ready_filter",
                self._state_filter_xpath,
                "after",
            )
        return view_arch

    @api.model
    def _view_add_ready_policy_field(self, view_arch):
        if self._automatically_insert_ready_policy_fields:
            policy_element_templates = [
                "ssi_transaction_ready_mixin.ready_policy_field",
            ]
            for template in policy_element_templates:
                view_arch = self._add_view_element(
                    view_arch,
                    template,
                    self._policy_field_xpath,
                    "before",
                )
        return view_arch

    @api.model
    def _view_add_ready_button(self, view_arch):
        if self._automatically_insert_ready_button:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_ready_mixin.button_ready",
                "/form/header/field[@name='state']",
                "before",
            )
        return view_arch

    @ssi_decorator.insert_on_tree_view()
    def _01_view_add_tree_ready_button(self, view_arch):
        if self._automatically_insert_ready_button:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_ready_mixin.tree_button_ready",
                "/list/header",
                "inside",
            )
        return view_arch
