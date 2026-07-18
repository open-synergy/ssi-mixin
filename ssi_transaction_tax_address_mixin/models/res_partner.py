# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ResPartner(models.AbstractModel):
    """
    Extends ``res.partner`` to add ``'tax'`` as a valid contact type in the
    ``type`` selection field, making it possible to mark a partner contact
    as a dedicated tax address used by ``mixin.transaction_tax_address``.
    """

    _name = "res.partner"
    _inherit = [
        "res.partner",
    ]

    type = fields.Selection(
        selection_add=[
            ("tax", "Tax Address"),
        ],
    )
