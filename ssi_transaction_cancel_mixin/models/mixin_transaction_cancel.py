# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MixinTransactionCancel(models.AbstractModel):
    _name = "mixin.transaction_cancel"
    _inherit = [
        "mixin.transaction",
    ]
    _description = "Transaction Mixin - Cancel State Mixin"
    _cancel_state = "cancel"

    cancel_reason_id = fields.Many2one(
        string="Cancel Reason",
        comodel_name="base.cancel_reason",
        readonly=True,
    )

    def _compute_policy(self):
        _super = super(MixinTransactionCancel, self)
        _super._compute_policy()

    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )

    def _prepare_cancel_data(self, cancel_reason=False):
        self.ensure_one()
        return {
            "state": "cancel",
            "cancel_reason_id": cancel_reason and cancel_reason.id or False,
        }

    def action_cancel(self, cancel_reason=False):
        for record in self:
            record.write(record._prepare_cancel_data(cancel_reason))

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
