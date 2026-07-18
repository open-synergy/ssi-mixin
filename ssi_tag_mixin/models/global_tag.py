# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class GlobalTag(models.Model):
    """
    Master-data model (inheriting ``mixin.master_data``) representing a single
    global tag with an optional colour (inherited from its category) and a
    sequence for ordering.
    """

    _name = "global_tag"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Global Tag"
    _order = "id, sequence"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="global_tag_category",
        required=True,
    )
    color = fields.Integer(
        related="category_id.color",
    )
