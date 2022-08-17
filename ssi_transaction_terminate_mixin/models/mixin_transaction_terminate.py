# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree

from odoo import api, fields, models


class MixinTransactionTerminate(models.AbstractModel):
    _name = "mixin.transaction_terminate"
    _inherit = [
        "mixin.transaction",
    ]
    _description = "Transaction Mixin - Terminate State Mixin"
    _cancel_state = "terminate"

    # Attributes related to automatic form view
    _automatically_insert_terminate_policy_fields = True
    _automatically_insert_terminate_button = True
    _automatically_insert_terminate_reason = True

    # Attributes related to add element on search view automatically
    _automatically_insert_terminate_filter = True

    # Attributes related to add element on tree view automatically
    _automatically_insert_terminate_state_badge_decorator = True

    terminate_reason_id = fields.Many2one(
        string="Terminate Reason",
        comodel_name="base.terminate_reason",
        readonly=True,
    )

    def _compute_policy(self):
        _super = super(MixinTransactionTerminate, self)
        _super._compute_policy()

    terminate_ok = fields.Boolean(
        string="Can Terminate",
        compute="_compute_policy",
    )

    def _prepare_terminate_data(self, terminate_reason=False):
        self.ensure_one()
        return {
            "state": "terminate",
            "terminate_reason_id": terminate_reason and terminate_reason.id or False,
        }

    def action_terminate(self, terminate_reason=False):
        for record in self.sudo():
            record.write(record._prepare_terminate_data(terminate_reason))

    def _prepare_restart_data(self):
        self.ensure_one()
        _super = super(MixinTransactionTerminate, self)
        result = _super._prepare_restart_data()
        result.update(
            {
                "terminate_reason_id": False,
            }
        )
        return result

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        result = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        view_model = self.env["ir.ui.view"]

        view_arch = etree.XML(result["arch"])

        if view_type == "form" and self._automatically_insert_view_element:
            view_arch = self._view_add_terminate_policy_field(view_arch)
            view_arch = self._view_add_terminate_button(view_arch)
            view_arch = self._view_add_terminate_reason(view_arch)
            view_arch = self._reorder_header_button(view_arch)
            view_arch = self._reorder_policy_field(view_arch)
        elif view_type == "tree" and self._automatically_insert_view_element:
            view_arch = self._add_terminate_state_badge_decorator(view_arch)
        elif view_type == "search" and self._automatically_insert_view_element:
            view_arch = self._add_terminate_filter_on_search_view(view_arch)
            view_arch = self._reorder_state_filter_on_search_view(view_arch)

        if view_id and result.get("base_model", self._name) != self._name:
            view_model = view_model.with_context(base_model_name=result["base_model"])
        new_arch, new_fields = view_model.postprocess_and_fields(
            self._name, view_arch, result["view_id"]
        )
        result["arch"] = new_arch
        new_fields.update(result["fields"])
        result["fields"] = new_fields

        return result

    @api.model
    def _add_terminate_state_badge_decorator(self, view_arch):
        if self._automatically_insert_terminate_state_badge_decorator:
            _xpath = "/tree/field[@name='state']"
            if len(view_arch.xpath(_xpath)) == 0:
                return view_arch
            node_xpath = view_arch.xpath(_xpath)[0]
            node_xpath.set("decoration-danger", "state == 'terminate'")
        return view_arch

    @api.model
    def _add_terminate_filter_on_search_view(self, view_arch):
        if self._automatically_insert_terminate_filter:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_terminate_mixin.terminate_filter",
                self._state_filter_xpath,
                "after",
            )
        return view_arch

    @api.model
    def _view_add_terminate_policy_field(self, view_arch):
        if self._automatically_insert_terminate_policy_fields:
            policy_element_templates = [
                "ssi_transaction_terminate_mixin.terminate_policy_field",
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
    def _view_add_terminate_button(self, view_arch):
        if self._automatically_insert_terminate_button:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_terminate_mixin.button_terminate",
                "/form/header/field[@name='state']",
                "before",
            )
        return view_arch

    @api.model
    def _view_add_terminate_reason(self, view_arch):
        if self._automatically_insert_terminate_reason:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_terminate_mixin.terminate_reason",
                "/form/sheet/div[@class='oe_left']/div[@class='oe_title']/h1",
                "after",
            )
        return view_arch