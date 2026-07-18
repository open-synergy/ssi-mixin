# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class TestSequence(models.Model):
    """Concrete fixture model that inherits ``mixin.sequence`` so the abstract
    mixin can be exercised by the in-module test suite. It is intentionally
    kept minimal (no views, no menu, no ``mail.thread``) to avoid adding any
    production dependency or UI to the mixin module."""

    _name = "test.sequence"
    _description = "Test Sequence"
    _inherit = [
        "mixin.sequence",
    ]

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
    )
    date = fields.Date(
        string="Date",
        index=True,
        copy=False,
        default=fields.Date.context_today,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    notes = fields.Text(
        string="Notes",
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            record._create_sequence()
        return records
