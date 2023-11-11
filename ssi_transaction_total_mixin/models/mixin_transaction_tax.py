# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MixinTransactionTax(models.AbstractModel):
    _name = "mixin.transaction_tax"
    _inherit = [
        "mixin.transaction",
    ]
    _description = "Transaction Mixin - Tax Amount"

    _tax_detail_object_name = "tax_ids"
    _tax_detail_amount_field_name = "tax_amount"
    _amount_tax_field_name = "amount_tax"

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
    )
    amount_tax = fields.Monetary(
        compute="_compute_amount_tax",
        string="Tax Amount",
        currency_field="currency_id",
        store=True,
    )

    def _get_amount_tax_trigger(self):
        result = [
            self._tax_detail_object_name,
            self._tax_detail_object_name + "." + self._tax_detail_amount_field_name,
        ]
        return result

    @api.depends(lambda self: self._get_amount_tax_trigger())
    def _compute_amount_tax(self):
        for record in self:
            amount_tax = 0.0

            for tax in getattr(record, self._tax_detail_object_name):
                amount_tax += getattr(tax, self._tax_detail_amount_field_name)

            setattr(record, self._amount_tax_field_name, amount_tax)


class MixinTransactionTaxWithField(models.AbstractModel):
    _name = "mixin.transaction_tax_with_field"
    _inherit = [
        "mixin.transaction_tax",
    ]
    _description = "Transaction Mixin - Tax Amount With Field"

    _amount_tax_field_name = "amount_tax"

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
    )
    amount_tax = fields.Monetary(
        compute="_compute_amount_tax",
        string="Tax Amount",
        currency_field="currency_id",
        store=True,
    )
