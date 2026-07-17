# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MixinDatetimeDuration(models.AbstractModel):
    """
    Lightweight mixin that adds plain ``Datetime`` start and end fields
    (``date_start`` and ``date_end``) to any model that needs to record a
    datetime-level duration without the extended configuration overhead of
    ``mixin.date_duration``.
    """

    _name = "mixin.datetime_duration"
    _description = "Datetime Duration Mixin"

    date_start = fields.Datetime(
        string="Date Start",
    )
    date_end = fields.Datetime(
        string="Date End",
    )
