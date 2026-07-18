# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestBaseLostReason(YamlTransactionCase):
    def test_base_lost_reason(self):
        self.run_yaml_scenario("test_data_base_lost_reason.yaml")
