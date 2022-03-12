# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class MixinMasterData(models.AbstractModel):
    _name = "mixin.master_data"
    _description = "Mixin for Master Data"
    _field_name_string = "Name"

    @api.model
    def _get_field_name_string(self):
        return self._field_name_string

    name = fields.Char(
        string="Name",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
