# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DataRequirementType(models.Model):
    """
    Master-data model (inheriting ``mixin.master_data``) that classifies data
    requirements by type (e.g. “KTP”, “NPWP”) and associates them with a
    ``data_requirement_type_category``.
    """

    _name = "data_requirement_type"
    _description = "Data Requirement Type"
    _inherit = ["mixin.master_data"]

    mode = fields.Selection(
        string="Mode",
        selection=[
            ("url", "URL"),
            ("attachment", "Attachment"),
            ("text", "Free Text"),
        ],
        required=True,
        default="url",
    )
    text_template = fields.Text(
        string="Text Template",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="data_requirement_type_category",
    )
    duration_id = fields.Many2one(
        string="Duration",
        comodel_name="base.duration",
    )
    instruction_url = fields.Char(
        string="Instruction URL",
    )
