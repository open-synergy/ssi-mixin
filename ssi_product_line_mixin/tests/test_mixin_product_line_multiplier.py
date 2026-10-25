# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMixinProductLineMultiplier(YamlTransactionCase):
    """Cover ``mixin.product_line_multiplier`` and its factor mixin.

    Both mixins are AbstractModels, so the suite exercises them through
    the concrete fixtures ``test.product_line_multiplier`` and
    ``test.product_line_multiplier_factor`` (module
    ``test_ssi_product_line_mixin``).
    """

    def test_mixin_product_line_multiplier(self):
        """Run the multiplier quantity, constraint and cascade scenarios.

        Skip loudly when the fixture module is not installed instead of
        failing with an obscure KeyError.
        """
        if "test.product_line_multiplier" not in self.env:
            self.skipTest(
                "Model 'test.product_line_multiplier' is not available - "
                "module 'test_ssi_product_line_mixin' is not installed."
            )
        self.run_yaml_scenario("test_data_mixin_product_line_multiplier.yaml")
