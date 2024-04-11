# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class IrModel(models.Model):
    _name = "ir.model"
    _inherit = "ir.model"

    global_tag_category_ids = fields.Many2many(
        string="Global Tag Categories",
        comodel_name="global_tag_category",
        relation="rel_model_2_global_tag_category",
        column1="model_id",
        column2="global_tag_category_id",
    )

    def _compute_all_global_tag_category_ids(self):
        Category = self.env["global_tag_category"]
        criteria = [
            ("global_use", "=", True),
        ]
        categories = Category.search(criteria)
        for record in self:
            record.all_global_tag_category_ids = (
                categories + record.global_tag_category_ids
            ).ids

    all_global_tag_category_ids = fields.Many2many(
        string="All Global Tag Categories",
        comodel_name="global_tag_category",
        compute="_compute_all_global_tag_category_ids",
        store=False,
    )
