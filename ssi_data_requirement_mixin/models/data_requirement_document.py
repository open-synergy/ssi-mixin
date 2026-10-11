# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DataRequirementDocument(models.Model):  # pylint: disable=too-few-public-methods
    _name = "data_requirement.document"
    _description = "Data Requirement Document Link"

    res_model = fields.Char(
        string="Related Document Model",
        index=True,
        required=True,
    )
    res_id = fields.Integer(
        string="Related Document ID",
        index=True,
        required=True,
    )
    data_requirement_id = fields.Many2one(
        string="Data Requirement",
        comodel_name="data_requirement",
        required=True,
        ondelete="cascade",
    )
