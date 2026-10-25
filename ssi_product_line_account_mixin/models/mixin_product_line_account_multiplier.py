# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MixinProductLineAccountMultiplier(models.AbstractModel):
    """
    Abstract mixin combining accounting and multiplier on a product line.

    Inherits ``mixin.product_line_account`` and
    ``mixin.product_line_price_multiplier`` and adds nothing of its own.
    The multiplier chain redefines ``uom_quantity``, so the factors drive
    ``uom_quantity`` and, through the unchanged ``_compute_total``, also
    ``price_subtotal``, ``price_tax`` and ``price_total``.

    Installation contract: the concrete line model adds this mixin to its
    ``_inherit`` and defines ``multiplier_ids`` itself, a One2many to the
    concrete model inheriting ``mixin.product_line_multiplier_factor``.

    Do NOT install this mixin on a model that already defines its own
    ``uom_quantity``; the two definitions would conflict.
    """

    _name = "mixin.product_line_account_multiplier"
    _description = "Product Line Mixin - With Accounting and Multiplier"
    _inherit = [
        "mixin.product_line_account",
        "mixin.product_line_price_multiplier",
    ]
