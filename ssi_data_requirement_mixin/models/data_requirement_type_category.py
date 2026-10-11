# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class DataRequirementTypeCategory(models.Model):
    """
    Master-data model (inheriting ``mixin.master_data``) that groups
    ``data_requirement_type`` records into logical categories.
    """

    _name = "data_requirement_type_category"
    _description = "Data Requirement Type Category"
    _inherit = ["mixin.master_data"]
