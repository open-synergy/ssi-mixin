# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StateChangeConstrainTemplateDetail(models.Model):
    _name = "state.change.constrain.template_detail"
    _description = "Status Check Template Detail"
    _order = "sequence, id"

    template_id = fields.Many2one(
        string="State Change Constrain Template",
        comodel_name="state.change.constrain.template",
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        related="template_id.company_id",
        store=True,
    )
    state = fields.Char(
        string="State",
        required=True,
    )
    status_check_item_ids = fields.Many2many(
        string="Status Check Item",
        comodel_name="status.check.item",
        relation="rel_state_change_constrain_detail_check_item",
        column1="status_check_item_id",
        column2="state_change_constrain_detail_id",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=1,
    )
    active = fields.Boolean(
        default=True,
    )
