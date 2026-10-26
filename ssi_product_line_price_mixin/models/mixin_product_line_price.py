# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MixinProductLinePrice(models.AbstractModel):
    """
    Extends ``mixin.product_line`` with pricing fields: ``currency_id``,
    ``pricelist_id``, ``price_unit``, ``price_subtotal``, and standard-price
    comparison fields (``standard_price_unit``, ``standard_price_subtotal``,
    and their diff variants).

    A computed ``allowed_pricelist_ids`` filters available pricelists by the
    selected currency, and ``price_subtotal`` = ``price_unit`` * quantity.
    """

    _name = "mixin.product_line_price"
    _description = "Product Line Mixin - With Price"
    _inherit = "mixin.product_line"

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        required=True,
        default=lambda self: self._default_currency_id(),
    )
    allowed_pricelist_ids = fields.Many2many(
        string="Allowed Pricelists",
        comodel_name="product.pricelist",
        compute="_compute_allowed_pricelist_ids",
        compute_sudo=True,
    )
    pricelist_id = fields.Many2one(
        comodel_name="product.pricelist",
    )
    price_unit = fields.Monetary(
        currency_field="currency_id",
        required=True,
        default=0.0,
    )
    price_subtotal = fields.Monetary(
        currency_field="currency_id",
        compute="_compute_price",
        store=True,
    )
    standard_price_unit = fields.Monetary(
        currency_field="currency_id",
        compute="_compute_standard_price",
        store=True,
        compute_sudo=True,
    )
    standard_price_subtotal = fields.Monetary(
        currency_field="currency_id",
        compute="_compute_standard_price",
        store=True,
        compute_sudo=True,
    )
    standard_price_unit_diff = fields.Monetary(
        string="Standard Price Unit Diff.",
        currency_field="currency_id",
        compute="_compute_standard_price",
        store=True,
        compute_sudo=True,
    )
    standard_price_subtotal_diff = fields.Monetary(
        string="Standard Price Subtotal Diff.",
        currency_field="currency_id",
        compute="_compute_standard_price",
        store=True,
        compute_sudo=True,
    )

    @api.model
    def _default_currency_id(self):
        """Return the default currency.

        :return: id of the current company currency.
        :rtype: int
        """
        return self.env.company.currency_id.id

    @api.depends(
        "product_id",
        "pricelist_id",
        "price_unit",
        "uom_quantity",
        "uom_id",
    )
    def _compute_standard_price(self):
        """Compute the standard price fields from the pricelist.

        Fills ``standard_price_unit``, ``standard_price_subtotal`` and their
        diff counterparts. All values are zero without pricelist or product.
        """
        for record in self:
            standard_price_unit = standard_price_subtotal = standard_price_unit_diff = (
                standard_price_subtotal_diff
            ) = 0.0
            if record.pricelist_id and record.product_id:
                final_price, _rule_id = record.pricelist_id._get_product_price_rule(
                    record.product_id,
                    record.uom_quantity or 1.0,
                    uom=record.uom_id or None,
                )
                standard_price_unit = final_price
                standard_price_subtotal = standard_price_unit * record.uom_quantity
                standard_price_unit_diff = record.price_unit - standard_price_unit
                standard_price_subtotal_diff = (
                    record.price_subtotal - standard_price_subtotal
                )
            record.standard_price_unit = standard_price_unit
            record.standard_price_subtotal = standard_price_subtotal
            record.standard_price_unit_diff = standard_price_unit_diff
            record.standard_price_subtotal_diff = standard_price_subtotal_diff

    @api.depends(
        "currency_id",
    )
    def _compute_allowed_pricelist_ids(self):
        """Compute the pricelists matching the selected currency."""
        Pricelist = self.env["product.pricelist"]
        for record in self:
            result = []
            if record.currency_id:
                criteria = record._get_pricelist_domain()
                result = Pricelist.search(criteria).ids
            record.allowed_pricelist_ids = result

    @api.depends(
        "price_unit",
        "uom_quantity",
    )
    def _compute_price(self):
        """Compute ``price_subtotal`` as unit price times UoM quantity."""
        for record in self:
            record.price_subtotal = record.price_unit * record.uom_quantity

    @api.onchange(
        "allowed_pricelist_ids",
        "currency_id",
    )
    def onchange_pricelist_id(self):
        """Select the first allowed pricelist, or clear the pricelist."""
        self.pricelist_id = False
        if self.allowed_pricelist_ids:
            self.pricelist_id = self.allowed_pricelist_ids[0]._origin.id

    def _get_pricelist_domain(self):
        """Return the domain used to find the allowed pricelists.

        :return: search domain on ``product.pricelist``.
        :rtype: list
        """
        self.ensure_one()
        return [
            ("currency_id", "=", self.currency_id.id),
        ]

    @api.onchange(
        "product_id",
        "uom_quantity",
        "uom_id",
        "pricelist_id",
    )
    def onchange_price_unit(self):
        """Fill ``price_unit`` from the selected pricelist."""
        if self.product_id and self.pricelist_id:
            final_price, _rule_id = self.pricelist_id._get_product_price_rule(
                self.product_id,
                self.uom_quantity or 1.0,
                uom=self.uom_id or None,
            )
            self.price_unit = final_price
