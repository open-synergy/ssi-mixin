# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree

from odoo import api, fields, models


class MixinTransactionCancel(models.AbstractModel):
    _name = "mixin.transaction_cancel"
    _inherit = [
        "mixin.transaction",
    ]
    _description = "Transaction Mixin - Cancel State Mixin"
    _cancel_state = "cancel"

    # Attributes related to automatic form view
    _automatically_insert_cancel_policy_fields = True
    _automatically_insert_cancel_button = True
    _automatically_insert_cancel_reason = True

    # Attributes related to add element on search view automatically
    _automatically_insert_cancel_filter = True

    # Attributes related to add element on tree view automatically
    _automatically_insert_cancel_state_badge_decorator = True

    cancel_reason_id = fields.Many2one(
        string="Cancel Reason",
        comodel_name="base.cancel_reason",
        readonly=True,
    )

    @api.multi
    def _compute_policy(self):
        _super = super(MixinTransactionCancel, self)
        _super._compute_policy()

    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )

    @api.multi
    def _prepare_cancel_data(self, cancel_reason=False):
        self.ensure_one()
        return {
            "state": "cancel",
            "cancel_reason_id": cancel_reason and cancel_reason.id or False,
        }

    @api.multi
    def action_cancel(self, cancel_reason=False):
        for record in self:
            record.write(record._prepare_cancel_data(cancel_reason))

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        _super = super(MixinTransactionCancel, self)
        result = _super._prepare_restart_data()
        result.update(
            {
                "cancel_reason_id": False,
            }
        )
        return result

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        res = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        view_model = self.env["ir.ui.view"]
        view_arch = etree.XML(res["arch"])
        if view_type == "form" and self._automatically_insert_view_element:
            view_arch = self._view_add_cancel_policy_field(view_arch)
            view_arch = self._view_add_cancel_button(view_arch)
            view_arch = self._view_add_cancel_reason(view_arch)
            view_arch = self._reorder_header_button(view_arch)
            view_arch = self._reorder_policy_field(view_arch)
        elif view_type == "tree" and self._automatically_insert_view_element:
            view_arch = self._add_cancel_state_badge_decorator(view_arch)
        elif view_type == "search" and self._automatically_insert_view_element:
            view_arch = self._add_cancel_filter_on_search_view(view_arch)
            view_arch = self._reorder_state_filter_on_search_view(view_arch)

        if view_id and res.get("base_model", self._name) != self._name:
            view_model = view_model.with_context(base_model_name=res["base_model"])
        new_arch, new_fields = view_model.postprocess_and_fields(
            self._name, view_arch, res["view_id"]
        )
        res["arch"] = new_arch
        new_fields.update(res["fields"])
        res["fields"] = new_fields
        return res

    @api.model
    def _add_cancel_state_badge_decorator(self, view_arch):
        if self._automatically_insert_cancel_state_badge_decorator:
            _xpath = "/tree/field[@name='state']"
            if len(view_arch.xpath(_xpath)) == 0:
                return view_arch
            node_xpath = view_arch.xpath(_xpath)[0]
            node_xpath.set("decoration-muted", "state == 'cancel'")
        return view_arch

    @api.model
    def _add_cancel_filter_on_search_view(self, view_arch):
        if self._automatically_insert_cancel_filter:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_cancel_mixin.cancel_filter",
                self._state_filter_xpath,
                "after",
            )
        return view_arch

    @api.model
    def _view_add_cancel_policy_field(self, view_arch):
        if self._automatically_insert_cancel_policy_fields:
            policy_element_templates = [
                "ssi_transaction_cancel_mixin.cancel_policy_field",
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
    def _view_add_cancel_button(self, view_arch):
        if self._automatically_insert_cancel_button:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_cancel_mixin.button_cancel",
                "/form/header/field[@name='state']",
                "before",
            )
        return view_arch

    @api.model
    def _view_add_cancel_reason(self, view_arch):
        if self._automatically_insert_cancel_reason:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_cancel_mixin.cancel_reason",
                "/form/sheet/div[@class='oe_left']/div[@class='oe_title']/h1",
                "after",
            )
        return view_arch
