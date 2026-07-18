# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CustomInfoProperty(models.Model):
    """
    Defines a single custom-information property: its name, code, data type
    (text, integer, decimal, boolean, selection, multiple-selection, date, or
    datetime), and an optional option set for selection-type properties.

    Properties are assigned to models through ``custom_info.template_detail``
    records on a ``custom_info.template``.
    """

    _name = "custom_info.property"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Custom information property"

    field_type = fields.Selection(
        selection=[
            ("str", "Text"),
            ("int", "Whole number"),
            ("float", "Decimal number"),
            ("bool", "Yes/No"),
            ("id", "Selection"),
            ("ids", "Multiple Selection"),
            ("date", "Date"),
            ("datetime", "Datetime"),
        ],
        default="str",
        required=True,
    )
    option_set_id = fields.Many2one(
        string="Option Set",
        comodel_name="custom_info.option_set",
    )
    option_ids = fields.Many2many(
        string="Options",
        comodel_name="custom_info.option",
        related="option_set_id.option_ids",
        store=False,
        readonly=True,
    )
