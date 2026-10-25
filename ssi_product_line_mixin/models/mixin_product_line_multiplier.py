# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MixinProductLineMultiplier(models.AbstractModel):
    """
    Abstract mixin that computes ``uom_quantity`` from multiplier factors.

    Inherits ``mixin.product_line`` and redefines ``uom_quantity`` as a
    stored, editable computed field: when the line has at least one
    factor it is the product of all factors; without factors the current
    value (manual or last computed) is kept.

    Installation contract: the concrete line model adds this mixin to its
    ``_inherit`` and defines ``multiplier_ids`` itself, a One2many to the
    concrete model inheriting ``mixin.product_line_multiplier_factor``
    with inverse ``line_id``. The depends on ``multiplier_ids`` is valid
    on this abstract model because abstract models are skipped when field
    triggers are built.

    Do NOT install this mixin on a model that already defines its own
    ``uom_quantity``; the two definitions would conflict.
    """

    _name = "mixin.product_line_multiplier"
    _description = "Product Line Multiplier Mixin"
    _inherit = [
        "mixin.product_line",
    ]

    @api.depends(
        "multiplier_ids",
        "multiplier_ids.factor",
    )
    def _compute_uom_quantity(self):
        """Compute ``uom_quantity`` as the product of all factors.

        Lines without factors keep their current ``uom_quantity``.
        """
        for record in self:
            result = record.uom_quantity
            if record.multiplier_ids:
                result = 1.0
                for factor in record.multiplier_ids:
                    result *= factor.factor
            record.uom_quantity = result

    uom_quantity = fields.Float(
        compute="_compute_uom_quantity",
        store=True,
        readonly=False,
    )
