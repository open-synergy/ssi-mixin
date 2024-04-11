# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class GlobalTagCategory(models.Model):
    _name = "global_tag_category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Global Tag Category"
    _order = "id, sequence"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
    )
    color = fields.Integer(
        string="Color Index",
    )
    exclusive = fields.Boolean(
        string="Exclusive",
    )
    global_use = fields.Boolean(
        string="Global Use",
        default=False,
    )
