# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MixinTransactionTotal(models.AbstractModel):
    """
    Extends ``mixin.transaction`` with a computed ``amount_total`` monetary
    field and a ``currency_id``.

    The amounts are aggregated from configurable detail-line fields controlled
    by ``_amount_untaxed_field_name``, ``_amount_tax_field_name``, and
    ``_amount_total_field_name`` class attributes.

    ``MixinTransactionTotalWithField`` is a variant that adds the amount
    fields to the underlying database columns.
    """

    _name = "mixin.transaction_total"
    _inherit = [
        "mixin.transaction",
    ]
    _description = "Transaction Mixin - Total"

    _amount_untaxed_field_name = "amount_untaxed"
    _amount_tax_field_name = False
    _amount_total_field_name = "amount_total"

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
    )
    amount_total = fields.Monetary(
        compute="_compute_amount_total",
        string="Total Amount",
        currency_field="currency_id",
        store=True,
    )

    def _get_amount_total_trigger(self):
        result = [self._amount_untaxed_field_name]
        if self._amount_tax_field_name:
            result += [self._amount_tax_field_name]
        return result

    @api.depends(lambda self: self._get_amount_total_trigger())
    def _compute_amount_total(self):
        for record in self:
            amount_untaxed = amount_tax = amount_total = 0.0

            if self._amount_untaxed_field_name and hasattr(
                record, self._amount_untaxed_field_name
            ):
                amount_untaxed = getattr(record, self._amount_untaxed_field_name)

            if self._amount_tax_field_name and hasattr(
                record, self._amount_tax_field_name
            ):
                amount_tax = getattr(record, self._amount_tax_field_name)

            amount_total = amount_untaxed + amount_tax

            setattr(record, self._amount_total_field_name, amount_total)


class MixinTransactionTotalWithField(models.AbstractModel):
    _name = "mixin.transaction_total_with_field"
    _inherit = [
        "mixin.transaction_total",
    ]
    _description = "Transaction Mixin - Total With Total"

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
    )
    amount_total = fields.Monetary(
        compute="_compute_amount_total",
        string="Total Amount",
        currency_field="currency_id",
        store=True,
    )
