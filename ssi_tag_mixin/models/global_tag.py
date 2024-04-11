# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class GlobalTag(models.Model):
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
