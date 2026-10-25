# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MixinProductLinePriceMultiplier(models.AbstractModel):
    """
    Abstract mixin combining price and multiplier on a product line.

    Inherits ``mixin.product_line_price`` and
    ``mixin.product_line_multiplier`` and adds nothing of its own. Both
    parents meet in ``mixin.product_line``, and only the multiplier mixin
    redefines ``uom_quantity``, so the computed quantity wins: the factors
    drive ``uom_quantity`` and then ``price_subtotal``.

    Installation contract: the concrete line model adds this mixin to its
    ``_inherit`` and defines ``multiplier_ids`` itself, a One2many to the
    concrete model inheriting ``mixin.product_line_multiplier_factor``.

    Do NOT install this mixin on a model that already defines its own
    ``uom_quantity``; the two definitions would conflict.
    """

    _name = "mixin.product_line_price_multiplier"
    _description = "Product Line Mixin - With Price and Multiplier"
    _inherit = [
        "mixin.product_line_price",
        "mixin.product_line_multiplier",
    ]
