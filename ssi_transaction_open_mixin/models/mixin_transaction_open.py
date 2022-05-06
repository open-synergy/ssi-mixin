# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree

from odoo import api, fields, models


class MixinTransactionOpen(models.AbstractModel):
    _name = "mixin.transaction_open"
    _inherit = [
        "mixin.transaction",
    ]
    _description = "Transaction Mixin - In Progress State Mixin"
    _open_state = "open"
    _automatically_insert_open_policy_fields = True
    _automatically_insert_open_button = True
    _done_button_order = 60
    _open_policy_field_order = 20

    # Attributes related to add element on search view automatically
    _automatically_insert_cancel_filter = True

    def _compute_policy(self):
        _super = super(MixinTransactionOpen, self)
        _super._compute_policy()

    open_ok = fields.Boolean(
        string="Can Start",
        compute="_compute_policy",
    )

    def _prepare_open_data(self):
        self.ensure_one()
        result = {
            "state": self._open_state,
        }
        if self._create_sequence_state == self._open_state:
            self._create_sequence()
        return result

    def action_open(self):
        for record in self.sudo():
            record.write(record._prepare_open_data())

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
            view_arch = self._view_add_open_policy_field(view_type, view_arch)
            view_arch = self._view_add_open_button(view_type, view_arch)
            view_arch = self._reorder_header_button(view_arch, view_type)
            view_arch = self._reorder_policy_field(view_arch, view_type)
        elif view_type == "search" and self._automatically_insert_view_element:
            view_arch = self._add_open_filter_on_search_view(view_arch)
            view_arch = self._reorder_state_filter_on_search_view(view_arch)

        if view_id and result.get("base_model", self._name) != self._name:
            View = View.with_context(base_model_name=result["base_model"])
        new_arch, new_fields = View.postprocess_and_fields(view_arch, self._name)
        result["arch"] = new_arch
        new_fields.update(result["fields"])
        result["fields"] = new_fields

        return result

    @api.model
    def _view_add_open_policy_field(self, view_type, view_arch):
        if (
            view_type == "form"
            and self._automatically_insert_view_element
            and self._automatically_insert_open_policy_fields
        ):
            policy_element_templates = [
                "ssi_transaction_open_mixin.open_policy_field",
            ]
            for template in policy_element_templates:
                view_arch = self._add_view_element(
                    view_arch,
                    template,
                    self._policy_field_xpath,
                    "before",
                    self._open_policy_field_order,
                )
        return view_arch

    @api.model
    def _view_add_open_button(self, view_type, view_arch):
        if (
            view_type == "form"
            and self._automatically_insert_view_element
            and self._automatically_insert_open_button
        ):
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_open_mixin.button_open",
                "/form/header/field[@name='state']",
                "before",
                self._done_button_order,
            )
        return view_arch

    @api.model
    def _add_open_filter_on_search_view(self, view_arch):
        if self._automatically_insert_open_filter:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_open_mixin.open_filter",
                self._state_filter_xpath,
                "after",
            )
        return view_arch
