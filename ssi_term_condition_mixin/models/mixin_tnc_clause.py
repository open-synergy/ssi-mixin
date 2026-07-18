# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TncClauseMixin(models.AbstractModel):
    """
    Abstract base for T&C clause records, providing ``name``, ``title``,
    ``raw_content``, and ``sequence``.

    Concretised by both ``tnc_clause`` (document-instance clauses) and
    ``tnc_template.clause`` (template-level clauses).
    """

    _name = "mixin.tnc_clause"
    _description = "Mixin - Terms and Condition Clause"
    _order = "sequence, id"

    section_id = fields.Many2one(
        string="Section",
        comodel_name="mixin.tnc_section",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
    )
    name = fields.Char(
        string="Clause",
        required=True,
    )
    title = fields.Char(
        string="Title",
        required=True,
    )
    raw_content = fields.Text(
        string="Raw Content",
    )
    content = fields.Text(
        string="Content",
        compute="_compute_content",
        store=False,
        compute_sudo=True,
    )
