# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


# pylint: disable=too-few-public-methods
from odoo import fields, models


class MixinMultipleOperatingUnit(models.AbstractModel):
    _name = "mixin.multiple_operating_unit"
    _description = "Mixin for Object With Multiple Operating Unit"

    operating_unit_ids = fields.Many2many(
        string="Operating Unit",
        comodel_name="operating.unit",
        column2="operating_unit_id",
    )
