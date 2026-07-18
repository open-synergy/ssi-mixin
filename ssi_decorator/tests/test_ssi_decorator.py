# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSsiDecorator(YamlTransactionCase):
    def test_ssi_decorator(self):
        # "mixin.decorator" is an AbstractModel and cannot be instantiated
        # directly. This suite exercises it through the concrete fixture
        # model "test.decorator", which is bundled inside this module (see
        # models/test_decorator.py) so the mixin is self-testing.
        self.run_yaml_scenario("test_data_ssi_decorator.yaml")
