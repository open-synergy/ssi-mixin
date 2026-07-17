# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MixinProductLine(models.AbstractModel):
    """
    Abstract mixin for product-line child records (detail rows) in a
    transactional document.

    Provides ``product_id``, ``name`` (description), ``uom_quantity``,
    ``uom_id``, and a computed ``quantity`` (converted to the product’s base
    UoM). Onchange handlers auto-fill the description and UoM from the
    selected product. The ``_field_for_name`` attribute controls which product
    field populates ``name``.
    """

    _name = "mixin.product_line"
    _description = "Product Line Mixin"
    _field_for_name = "display_name"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    product_category_id = fields.Many2one(
        string="Product Category", related="product_id.categ_id", store=True
    )
    name = fields.Char(
        string="Description",
        required=True,
    )
    uom_quantity = fields.Float(
        string="UoM Quantity",
        required=True,
        default=1.0,
    )

    @api.depends("product_id")
    def _compute_allowed_uom_ids(self):
        UoM = self.env["uom.uom"]
        for record in self:
            result = []
            if record.product_id:
                criteria = [
                    ("category_id", "=", record.product_id.uom_id.id),
                ]
                result = UoM.search(criteria).ids
            record.allowed_uom_ids = result

    allowed_uom_ids = fields.Many2many(
        string="Allowed UoMs",
        comodel_name="uom.uom",
        compute="_compute_allowed_uom_ids",
        compute_sudo=True,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="uom.uom",
    )

    @api.depends(
        "uom_id",
        "product_id",
        "uom_quantity",
    )
    def _compute_qty(self):
        for record in self:
            result = record.uom_quantity
            if record.uom_id and record.product_id:
                product_uom_id = record.product_id.uom_id
                result = record.uom_id._compute_quantity(
                    record.uom_quantity, product_uom_id
                )
            record.quantity = result

    quantity = fields.Float(
        string="Quantity",
        required=False,
        compute="_compute_qty",
        store=True,
    )
    note = fields.Text(
        string="Note",
    )

    @api.onchange(
        "product_id",
    )
    def onchange_name(self):
        self.name = False
        if self.product_id:
            self.name = getattr(self.product_id, self._field_for_name)

    @api.onchange(
        "product_id",
    )
    def onchange_uom_id(self):
        self.uom_id = False
        if self.product_id:
            self.uom_id = self.product_id.uom_id

    @api.onchange(
        "product_id",
    )
    def onchange_sequence(self):
        self.sequence = 0
        if self.product_id:
            self.sequence = self.product_id.sequence
