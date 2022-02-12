# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StateChangeHistory(models.Model):
    _name = "state.change.history"
    _description = "State Change History"

    model = fields.Char(
        string="Related Document Model",
        index=True,
    )
    res_id = fields.Integer(
        string="Related Document ID",
        index=True,
    )
    user_id = fields.Many2one(
        string="User",
        comodel_name="res.users",
        required=True,
    )
    state_from = fields.Char(
        string="State From",
        required=True,
    )
    state_to = fields.Char(
        string="State To",
        required=True,
    )
    date_change = fields.Datetime(
        string="Date Change",
        required=True,
    )
