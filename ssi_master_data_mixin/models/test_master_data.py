# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class TestMasterData(models.Model):
    """Concrete fixture model that inherits ``mixin.master_data`` so the
    abstract mixin can be exercised by the in-module test suite. It is
    bundled inside this module (install-time) so the mixin is self-testing."""

    _name = "test.master_data"
    _description = "Test Master Data"
    _inherit = [
        "mixin.master_data",
    ]
