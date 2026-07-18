# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CustomInfoCategory(models.Model):
    """
    Master-data model representing a category for grouping custom information
    properties.

    Categories are used to organise ``custom_info.property`` records on the
    custom-information template so that related properties are visually grouped
    together on the form view.
    """

    _name = "custom_info.category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Categorize custom info properties"
    _order = "sequence, name"

    sequence = fields.Integer(
        index=True,
        default=5,
    )
