# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StatusCheckTemplateDetail(models.Model):
    _name = "status.check.template_detail"
    _description = "Status Check Template Detail"
    _order = "sequence, id"

    template_id = fields.Many2one(
        string="Status Check Template",
        comodel_name="status.check.template",
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        related="template_id.company_id",
        store=True,
    )
    sequence = fields.Integer(
        default=5,
        required=True,
    )
    status_check_item_id = fields.Many2one(
        string="Status Check Item",
        comodel_name="status.check.item",
        ondelete="restrict",
        required=True,
    )
    active = fields.Boolean(
        default=True,
    )
