# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MixinTransactionPricelist(models.AbstractModel):
    """
    Composes ``mixin.transaction`` with ``mixin.pricelist`` to add
    ``currency_id`` and ``pricelist_id`` fields with draft-state editability
    controls to transactional documents.
    """

    _name = "mixin.transaction_pricelist"
    _inherit = [
        "mixin.transaction",
        "mixin.pricelist",
    ]
    _description = "Transaction + Pricelist Mixin"

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
