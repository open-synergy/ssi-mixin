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
        # model "test.policy", which is bundled inside this module (see
        # models/test_policy.py) so the mixin is self-testing.
        self.run_yaml_scenario("test_data_mixin_policy.yaml")
