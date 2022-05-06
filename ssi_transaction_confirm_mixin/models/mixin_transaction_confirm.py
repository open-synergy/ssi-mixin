# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree

from odoo import api, fields, models


class MixinTransactionConfirm(models.AbstractModel):
    _name = "mixin.transaction_confirm"
    _inherit = [
        "mixin.transaction",
        "mixin.multiple_approval",
    ]
    _description = "Transaction Mixin - Waiting for Approval Mixin"
    _confirm_state = "confirm"

    # Attributes related to automatic form view
    _automatically_insert_confirm_policy_fields = True
    _automatically_insert_confirm_button = True
    _automatically_insert_approve_button = True
    _automatically_insert_reject_button = True
    _confirm_button_order = 10
    _approve_button_order = 20
    _reject_button_order = 30
    _confirm_policy_field_order = 10

    # Attributes related to add element on search view automatically
    _automatically_insert_confirm_filter = True
    _automatically_insert_reject_filter = True

    def _compute_policy(self):
        _super = super(MixinTransactionConfirm, self)
        _super._compute_policy()

    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    approve_ok = fields.Boolean(
        string="Can Approve",
        compute="_compute_policy",
    )
    reject_ok = fields.Boolean(
        string="Can Reject",
        compute="_compute_policy",
    )
    restart_approval_ok = fields.Boolean(
        string="Can Restart Approval",
        compute="_compute_policy",
    )

    def action_confirm(self):
        for record in self.sudo():
            record.write(record._prepare_confirm_data())
            record.action_request_approval()

    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": self._confirm_state,
        }

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        result = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        View = self.env["ir.ui.view"]

        view_arch = etree.XML(result["arch"])
        if view_type == "form":
            view_arch = self._view_add_policy_field(view_type, view_arch)
            view_arch = self._view_add_confirm_button(view_type, view_arch)
            view_arch = self._view_add_approve_button(view_type, view_arch)
            view_arch = self._view_add_reject_button(view_type, view_arch)
            view_arch = self._reorder_header_button(view_arch, view_type)
            view_arch = self._reorder_policy_field(view_arch, view_type)
        elif view_type == "search" and self._automatically_insert_view_element:
            view_arch = self._add_confirm_filter_on_search_view(view_arch)
            view_arch = self._add_reject_filter_on_search_view(view_arch)
            view_arch = self._reorder_state_filter_on_search_view(view_arch)

        if view_id and result.get("base_model", self._name) != self._name:
            View = View.with_context(base_model_name=result["base_model"])
        new_arch, new_fields = View.postprocess_and_fields(view_arch, self._name)
        result["arch"] = new_arch
        new_fields.update(result["fields"])
        result["fields"] = new_fields

        return result

    @api.model
    def _add_confirm_filter_on_search_view(self, view_arch):
        if self._automatically_insert_confirm_filter:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_confirm_mixin.confirm_filter",
                self._state_filter_xpath,
                "after",
            )
        return view_arch

    @api.model
    def _add_reject_filter_on_search_view(self, view_arch):
        if self._automatically_insert_reject_filter:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_confirm_mixin.reject_filter",
                self._state_filter_xpath,
                "after",
            )
        return view_arch

    @api.model
    def _view_add_policy_field(self, view_type, view_arch):
        if (
            view_type == "form"
            and self._automatically_insert_view_element
            and self._automatically_insert_confirm_policy_fields
        ):
            policy_element_templates = [
                "ssi_transaction_confirm_mixin.confirm_policy_field",
                "ssi_transaction_confirm_mixin.approve_policy_field",
                "ssi_transaction_confirm_mixin.reject_policy_field",
                "ssi_transaction_confirm_mixin.restart_approval_policy_field",
            ]
            for template in policy_element_templates:
                view_arch = self._add_view_element(
                    view_arch,
                    template,
                    self._policy_field_xpath,
                    "before",
                    self._confirm_policy_field_order,
                )
        return view_arch

    @api.model
    def _view_add_confirm_button(self, view_type, view_arch):
        if (
            view_type == "form"
            and self._automatically_insert_view_element
            and self._automatically_insert_confirm_button
        ):
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_confirm_mixin.button_confirm",
                "/form/header/field[@name='state']",
                "before",
                self._confirm_button_order,
            )
        return view_arch

    @api.model
    def _view_add_approve_button(self, view_type, view_arch):
        if (
            view_type == "form"
            and self._automatically_insert_view_element
            and self._automatically_insert_approve_button
        ):
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_confirm_mixin.button_approve",
                "/form/header/field[@name='state']",
                "before",
                self._approve_button_order,
            )
        return view_arch

    @api.model
    def _view_add_reject_button(self, view_type, view_arch):
        if (
            view_type == "form"
            and self._automatically_insert_view_element
            and self._automatically_insert_reject_button
        ):
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_confirm_mixin.button_reject",
                "/form/header/field[@name='state']",
                "before",
                self._reject_button_order,
            )
        return view_arch
