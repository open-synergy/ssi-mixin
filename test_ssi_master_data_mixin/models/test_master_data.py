# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class TestMasterData(models.Model):
    _name = "test.master_data"
    _description = "Test Master Data"
    _inherit = [
        "mixin.master_data",
    ]
