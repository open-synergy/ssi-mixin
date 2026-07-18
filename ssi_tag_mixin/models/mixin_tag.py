# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MixinTag(models.AbstractModel):
    """
    Abstract mixin that adds global-tag support to any model.

    Models inheriting ``mixin.tag`` gain:

    * ``allowed_global_tag_category_ids`` — computed from the model’s
      ``ir.model`` record (merging ``global_use`` categories with model-specific
      ones).
    * ``global_tag_ids`` — Many2many to ``global_tag`` for storing the
      applied tags.
    """

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
