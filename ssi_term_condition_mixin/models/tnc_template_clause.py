# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TncTemplateClause(models.Model):
    """
    Template-level T&C clause (inheriting ``mixin.tnc_clause``) linked to a
    ``tnc_template.section`` record.

    Provides ``_create_tnc_clause`` to instantiate a ``tnc_clause`` on a
    document from the template content.
    """

    _name = "tnc_template.clause"
    _inherit = [
        "mixin.tnc_clause",
    ]
    _description = "T&C Template Clause"
    _order = "sequence, id"

    section_id = fields.Many2one(
        string="Section",
        comodel_name="tnc_template.section",
        required=True,
        ondelete="cascade",
    )

    def _create_tnc_clause(self, tnc_section):
        self.ensure_one()
        TNCClause = self.env["tnc_clause"]
        TNCClause.create(self._prepare_tnc_clause(tnc_section))

    def _prepare_tnc_clause(self, tnc_section):
        self.ensure_one()
        return {
            "section_id": tnc_section.id,
            "name": self.name,
            "title": self.title,
            "sequence": self.sequence,
            "raw_content": self.raw_content,
        }
