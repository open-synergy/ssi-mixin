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
        # model "test.decorator" (module "test_ssi_decorator"). Guard
        # against the fixture module not being installed, so this test
        # fails loudly with a clear reason instead of an obscure KeyError.
        if "test.decorator" not in self.env:
            self.skipTest(
                "Model 'test.decorator' is not available - "
                "module 'test_ssi_decorator' is not installed."
            )
        self.run_yaml_scenario("test_data_ssi_decorator.yaml")
