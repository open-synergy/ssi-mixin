# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MixinTransactionDateDue(models.AbstractModel):
    _name = "mixin.transaction_date_due"
    _inherit = [
        "mixin.transaction",
    ]
    _description = "Transaction Mixin - Date Due Mixin"

    date = fields.Date(
        string="Date",
        default=lambda r: r._default_date(),
        required=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    duration_id = fields.Many2one(
        string="Duration",
        comodel_name="base.duration",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_due = fields.Date(
        string="Date Due",
        required=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.model
    def _default_date(self):
        return fields.Date.today()

    @api.onchange(
        "duration_id",
        "date",
    )
    def onchange_date_due(self):
        self.date_due = False
        if self.duration_id:
            self.date_due = self.duration_id.get_duration(self.date)
