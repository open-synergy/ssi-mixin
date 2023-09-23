# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MixinTransactionResidual(models.AbstractModel):
    _name = "mixin.transaction_residual"
    _inherit = [
        "mixin.transaction",
    ]
    _description = "Transaction Mixin - Total Residual"

    _amount_residual_aml_field_name = "move_line_id"
    _amount_residual_sign = -1.0
    _amount_total_field_name = "amount_total"
    _amount_residual_field_name = "amount_residual"
    _amount_realized_field_name = "amount_realized"

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
    )
    amount_residual = fields.Monetary(
        compute="_compute_amount_residual",
        string="Residual Amount",
        currency_field="currency_id",
        store=True,
    )
    amount_realized = fields.Monetary(
        compute="_compute_amount_residual",
        string="Realized Amount",
        currency_field="currency_id",
        store=True,
    )

    def _get_amount_residual_trigger(self):
        result = [
            self._amount_total_field_name,
            self._amount_residual_aml_field_name,
            self._amount_residual_aml_field_name + ".amount_residual_currency",
            self._amount_residual_aml_field_name + ".reconciled",
        ]

        return result

    @api.depends(lambda self: self._get_amount_residual_trigger())
    def _compute_amount_residual(self):
        for record in self:
            amount_residual = amount_realized = amount_total = 0.0

            if hasattr(record, self._amount_total_field_name):
                amount_total = getattr(record, self._amount_total_field_name)

            if hasattr(record, self._amount_residual_aml_field_name):
                if getattr(record, self._amount_residual_aml_field_name):
                    aml = getattr(record, self._amount_residual_aml_field_name)
                    amount_residual = (
                        self._amount_residual_sign * aml.amount_residual_currency
                    )
                else:
                    amount_residual = amount_total

            amount_realized = amount_total - amount_residual

            setattr(record, self._amount_residual_field_name, amount_residual)
            setattr(record, self._amount_realized_field_name, amount_realized)


class MixinTransactionResidualWithField(models.AbstractModel):
    _name = "mixin.transaction_residual_with_field"
    _inherit = [
        "mixin.transaction_residual",
    ]
    _description = "Transaction Mixin - Total Residual With Field"

    _amount_residual_aml_field_name = "move_line_id"
    _amount_residual_sign = -1.0
    _amount_total_field_name = "amount_total"
    _amount_residual_field_name = "amount_residual"
    _amount_realized_field_name = "amount_realized"

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
    )
    amount_residual = fields.Monetary(
        compute="_compute_amount_residual",
        string="Residual Amount",
        currency_field="currency_id",
        store=True,
    )
    amount_realized = fields.Monetary(
        compute="_compute_amount_residual",
        string="Realized Amount",
        currency_field="currency_id",
        store=True,
    )
