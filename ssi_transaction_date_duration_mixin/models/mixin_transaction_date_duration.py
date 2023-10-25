# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class MixinTransactionDateDuration(models.AbstractModel):
    _name = "mixin.transaction_date_duration"
    _inherit = [
        "mixin.transaction",
    ]
    _description = "Mixin for Transaction Object Date Duration"

    date_start = fields.Date(
        string="Date Start",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
