# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MixinTransactionConfirm(models.AbstractModel):
    _name = "mixin.transaction_confirm"
    _inherit = [
        "mixin.transaction",
        "mixin.multiple_approval",
    ]
    _description = "Transaction Mixin - Waiting for Approval Mixin"
    _confirm_state = "confirm"

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
        for record in self:
            record.write(record._prepare_confirm_data())
            record.action_request_approval()

    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": self._confirm_state,
        }
