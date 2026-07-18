# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMixinSequence(YamlTransactionCase):
    def test_mixin_sequence(self):
        # "mixin.sequence" is an AbstractModel and cannot be instantiated
        # directly. This suite exercises it through the concrete fixture
        # model "test.sequence", which is bundled inside this module (see
        # models/test_sequence.py) so the mixin is self-testing.
        self.run_yaml_scenario("test_data_mixin_sequence.yaml")
