# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


# pylint: disable=too-few-public-methods
from odoo import models


class IrSequence(models.Model):
    _name = "ir.sequence"
    _inherit = [
        "ir.sequence",
        "mixin.multiple_operating_unit",
    ]
