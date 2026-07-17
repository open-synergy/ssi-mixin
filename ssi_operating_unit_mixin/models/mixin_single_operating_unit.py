# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MixinSingleOperatingUnit(models.AbstractModel):
    """
    Lightweight mixin that adds a single ``operating_unit_id`` Many2one field
    (``operating.unit``) to any model, defaulting to the current user’s
    default operating unit.
    """

    _name = "mixin.single_operating_unit"
    _description = "Mixin for Object With Single Operating Unit"

    operating_unit_id = fields.Many2one(
        string="Operating Unit",
        comodel_name="operating.unit",
        default=lambda self: self.env["res.users"].operating_unit_default_get(),
    )
