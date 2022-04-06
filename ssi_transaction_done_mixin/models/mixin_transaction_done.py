# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MixinTransactionDone(models.AbstractModel):
    _name = "mixin.transaction_done"
    _inherit = [
        "mixin.transaction",
    ]
    _description = "Transaction Mixin - Done State Mixin"
    _done_state = "done"

    def _compute_policy(self):
        _super = super(MixinTransactionDone, self)
        _super._compute_policy()

    done_ok = fields.Boolean(
        string="Can Finished",
        compute="_compute_policy",
    )

    def _prepare_done_data(self):
        self.ensure_one()
        result = {
            "state": self._done_state,
        }
        if self._create_sequence_state == self._done_state:
            self._create_sequence()
        return result

    def action_done(self):
        for record in self:
            record.write(record._prepare_done_data())
