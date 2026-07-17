# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMixinPolicy(YamlTransactionCase):
    def test_mixin_policy(self):
        # "mixin.policy" is an AbstractModel and cannot be instantiated
        # directly. This suite exercises it through the concrete fixture
        # model "test.policy" (module "test_ssi_policy_mixin"). Guard
        # against the fixture module not being installed, so this test fails
        # loudly with a clear reason instead of an obscure KeyError.
        if "test.policy" not in self.env:
            self.skipTest(
                "Model 'test.policy' is not available - module "
                "'test_ssi_policy_mixin' is not installed."
            )
        self.run_yaml_scenario("test_data_mixin_policy.yaml")
