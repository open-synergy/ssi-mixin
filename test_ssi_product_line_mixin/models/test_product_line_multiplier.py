# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TestProductLineMultiplier(models.Model):
    """Concrete fixture line using ``mixin.product_line_multiplier``."""

    _name = "test.product_line_multiplier"
    _description = "Test Product Line Multiplier"
    _inherit = [
        "mixin.product_line_multiplier",
    ]

    multiplier_ids = fields.One2many(
        string="Multipliers",
        comodel_name="test.product_line_multiplier_factor",
        inverse_name="line_id",
        help="Factors multiplied into the line quantity.",
    )
