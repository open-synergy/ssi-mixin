# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MixinTransactionUntaxed(models.AbstractModel):
    _name = "mixin.transaction_untaxed"
    _inherit = [
        "mixin.transaction",
    ]
    _description = "Transaction Mixin - Untaxed Amount"

    _detail_object_name = "detail_ids"
    _detail_amount_field_name = "price_subtotal"
    _amount_untaxed_field_name = "amount_untaxed"

    def _get_amount_untaxed_trigger(self):
        result = [
            self._detail_object_name,
            self._detail_object_name + "." + self._detail_amount_field_name,
        ]
        return result

    @api.depends(lambda self: self._get_amount_untaxed_trigger())
    def _compute_amount_untaxed(self):
        for record in self:
            amount_untaxed = 0.0

            for detail in getattr(record, self._detail_object_name):
                amount_untaxed += getattr(detail, self._detail_amount_field_name)

            setattr(record, self._amount_untaxed_field_name, amount_untaxed)


class MixinTransactionUntaxedWithField(models.AbstractModel):
    _name = "mixin.transaction_untaxed_with_field"
    _inherit = [
        "mixin.transaction_untaxed",
    ]
    _description = "Transaction Mixin - Untaxed Amount With Field"

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
    )
    amount_untaxed = fields.Monetary(
        compute="_compute_amount_untaxed",
        string="Untaxed Amount",
        currency_field="currency_id",
        store=True,
    )
