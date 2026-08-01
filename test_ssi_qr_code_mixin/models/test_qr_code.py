# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TestQrCode(models.Model):
    """
    Minimal concrete model exercising ``mixin.qr_code``.

    ``mixin.qr_code`` is an ``AbstractModel`` and cannot be
    instantiated directly, so the unit tests of ``ssi_qr_code_mixin``
    run against this fixture model instead.
    """

    _name = "test.qr_code"
    _description = "Test QR Code"
    _inherit = [
        "mixin.qr_code",
    ]

    name = fields.Char(
        string="Name",
        required=True,
    )
