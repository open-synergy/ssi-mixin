# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MixinTransactionOpen(models.AbstractModel):
    _name = "mixin.transaction_open"
    _inherit = [
        "mixin.transaction",
    ]
    _description = "Transaction Mixin - In Progress State Mixin"
    _open_state = "open"

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
            "state": "open",
        }
        if self._create_sequence_state == self._open_state:
            sequence = self._create_sequence()
            result.update(
                {
                    "name": sequence,
                }
            )
        return result

    def action_open(self):
        for record in self:
            record.write(record._prepare_open_data())
