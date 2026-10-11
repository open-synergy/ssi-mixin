# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DataRequirementPackageType(models.Model):
    """
    Master-data model (inheriting ``mixin.master_data``) that classifies data
    requirement packages into named types, each with an optional ordered list
    of ``data_requirement_type`` records (``detail_ids``).
    """

    _name = "data_requirement_package_type"
    _description = "Data Requirement Package Type"
    _inherit = ["mixin.master_data"]

    detail_ids = fields.One2many(
        string="Detail",
        comodel_name="data_requirement_package_type.detail",
        inverse_name="type_id",
    )
