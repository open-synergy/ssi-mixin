# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ReferenceDocumentSet(models.Model):
    """
    Master-data model (inheriting ``mixin.master_data``) that groups a
    collection of ``reference_document`` records into a named set.

    Sets are attached to documents via
    ``mixin.reference_document.reference_document_set_ids`` and the mixin
    flattens all documents across the linked sets for display.
    """

    _name = "reference_document_set"
    _description = "Reference Document Set"
    _inherit = ["mixin.master_data"]

    reference_document_ids = fields.Many2many(
        string="Reference Documents",
        comodel_name="reference_document",
        relation="rel_reference_document_set_2_document",
        column1="set_id",
        column2="document_id",
    )
