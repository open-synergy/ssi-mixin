# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class IrSequence(models.Model):
    """
    Extends ``ir.sequence`` with ``mixin.multiple_operating_unit`` so that
    sequences can optionally be restricted to specific operating units.
    """

    _name = "ir.sequence"
    _inherit = [
        "ir.sequence",
        "mixin.multiple_operating_unit",
    ]
