# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class MixinTag(models.AbstractModel):
    _name = "mixin.tag"
    _description = "Tax Mixin"

    allowed_global_tag_category_ids = fields.Many2many(
        string="Allowed Global Tag Categories",
        comodel_name="global_tag_category",
        compute="_compute_allowed_global_tag_category_ids",
        store=False,
    )

    @api.depends()
    def _compute_allowed_global_tag_category_ids(self):
        for record in self:
            model = self.env["ir.model"].search([("model", "=", self._name)])[0]
            record.allowed_global_tag_category_ids = model.all_global_tag_category_ids

    global_tag_ids = fields.Many2many(
        string="Global Tags",
        comodel_name="global_tag",
        column1="model_id",
        column2="tag_id",
    )
