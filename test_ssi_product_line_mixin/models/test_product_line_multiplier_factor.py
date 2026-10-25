# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TestProductLineMultiplierFactor(models.Model):
    """Concrete fixture factor using ``mixin.product_line_multiplier_factor``."""

    _name = "test.product_line_multiplier_factor"
    _description = "Test Product Line Multiplier Factor"
    _inherit = [
        "mixin.product_line_multiplier_factor",
    ]

    line_id = fields.Many2one(
        string="Line",
        comodel_name="test.product_line_multiplier",
        required=True,
        ondelete="cascade",
        help="Line this factor belongs to.",
    )
