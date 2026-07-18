# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TncSectionMixin(models.AbstractModel):
    """
    Abstract base for T&C section records, providing ``name``, ``title``,
    ``raw_content``, ``sequence``, and a ``clause_ids`` One2many.

    Concretised by both ``tnc_section`` (document-instance sections) and
    ``tnc_template.section`` (template-level sections).
    """

    _name = "mixin.tnc_section"
    _description = "Mixin - Terms and Condition Section"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
    )
    name = fields.Char(
        string="Section",
        required=True,
    )
    title = fields.Char(
        string="Title",
        required=True,
    )
    raw_content = fields.Text(
        string="Raw Content",
    )
    clause_ids = fields.One2many(
        string="Clauses",
        comodel_name="mixin.tnc_clause",
        inverse_name="section_id",
        copy=True,
    )
