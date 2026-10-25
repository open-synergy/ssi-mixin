# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MixinProductLineMultiplierFactor(models.AbstractModel):
    """
    Abstract mixin for one multiplier factor row of a product line.

    Each row holds a named factor (for example persons, days or times).
    The product of all factors of a line becomes the line's
    ``uom_quantity`` (see ``mixin.product_line_multiplier``).

    Installation contract: the concrete model must inherit this mixin and
    define ``line_id`` itself, a required Many2one to the concrete line
    model with ``ondelete="cascade"``. ``line_id`` is intentionally not
    defined here because the comodel differs for every user.
    """

    _name = "mixin.product_line_multiplier_factor"
    _description = "Product Line Multiplier Factor Mixin"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Display order of the factor within its line.",
    )
    name = fields.Char(
        string="Name",
        required=True,
        help="Label of the factor, for example Persons or Days.",
    )
    factor = fields.Float(
        string="Factor",
        required=True,
        default=1.0,
        help="Value multiplied into the line quantity. Must be positive.",
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="uom.uom",
        help="Unit label of the factor. Informational only: it is not "
        "used in the calculation and no conversion is applied.",
    )

    @api.constrains("factor")
    def _check_factor(self):
        """Reject factors that are zero or negative.

        :raises ValidationError: if any ``factor`` is not positive.
        """
        for record in self:
            if record.factor <= 0.0:
                raise ValidationError(_("Factor must be greater than zero."))
