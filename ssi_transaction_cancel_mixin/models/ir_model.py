# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class IrModel(models.Model):
    _name = "ir.model"
    _inherit = "ir.model"

    cancel_reason_ids = fields.Many2many(
        string="Cancel Reasons",
        comodel_name="base.cancel_reason",
        relation="rel_model_2_cancel_reason",
        column1="model_id",
        column2="cancel_reason_id",
    )
