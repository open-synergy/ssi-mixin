# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MixinReferenceDocument(models.AbstractModel):
    _name = "mixin.reference_document"
    _description = "Reference Document Mixin"

    reference_document_set_ids = fields.Many2many(
        string="Reference Document Sets",
        comodel_name="reference_document_set",
    )
    reference_document_ids = fields.Many2many(
        string="Reference Document",
        comodel_name="reference_document",
        compute="_compute_reference_document_ids",
        store=False,
        compute_sudo=True,
    )

    @api.depends(
        "reference_document_set_ids",
    )
    def _compute_reference_document_ids(self):
        for record in self.sudo():
            result = self.env["reference_document"]
            for document_set in record.reference_document_set_ids:
                result += document_set.reference_document_ids
            record.reference_document_ids = result
