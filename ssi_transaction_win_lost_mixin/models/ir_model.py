# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IrModel(models.Model):
    """
    Extends ``ir.model`` with ``lost_reason_ids`` — the set of lost reasons
    applicable for a model — and provides a computed ``all_lost_reason_ids``
    that merges globally-applicable reasons with the model-specific ones.
    """

    _name = "ir.model"
    _inherit = "ir.model"

    lost_reason_ids = fields.Many2many(
        string="Lost Reasons",
        comodel_name="base.lost_reason",
        relation="rel_model_2_lost_reason",
        column1="model_id",
        column2="lost_reason_id",
    )

    def _compute_all_lost_reason_ids(self):
        obj_reason = self.env["base.lost_reason"]
        criteria = [
            ("global_use", "=", True),
        ]
        global_reasons = obj_reason.search(criteria)
        for record in self:
            record.all_lost_reason_ids = (global_reasons + record.lost_reason_ids).ids

    all_lost_reason_ids = fields.Many2many(
        string="All Lost Reasons",
        comodel_name="base.lost_reason",
        compute="_compute_all_lost_reason_ids",
        store=False,
    )
