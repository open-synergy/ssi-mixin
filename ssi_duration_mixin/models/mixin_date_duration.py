# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MixinDateDuration(models.AbstractModel):
    _name = "mixin.date_duration"
    _description = "Date Duration Mixin"

    date_start = fields.Date(
        string="Date Start",
    )
    date_end = fields.Date(
        string="Date End",
    )
