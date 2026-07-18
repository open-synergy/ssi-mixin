# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TestPolicyType(models.Model):
    """Concrete fixture model bundled inside this module so the abstract
    ``mixin.policy`` can be exercised by the in-module test suite. It is used
    by the tests as an unrelated model to prove that policy templates are
    scoped to their own model. Kept minimal (no views, no menu) to avoid
    adding any production dependency or UI to the mixin module."""

    _name = "test.policy.type"
    _description = "Test Policy Type"

    name = fields.Char(
        string="# Document",
        required=True,
    )
    code = fields.Char(
        string="Code",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    notes = fields.Text(
        string="Notes",
    )
