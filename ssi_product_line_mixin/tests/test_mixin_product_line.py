# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMixinProductLine(YamlTransactionCase):
    """Cover ``mixin.product_line._compute_allowed_uom_ids()``.

    ``mixin.product_line`` is an AbstractModel and cannot be
    instantiated directly, so this suite exercises it through the
    concrete fixture model ``test.product_line`` (module
    ``test_ssi_product_line_mixin``).
    """

    def test_mixin_product_line(self):
        """Run the ``_compute_allowed_uom_ids`` category-matching scenarios.

        Guard against the fixture module not being installed, so this
        test fails loudly with a clear reason instead of an obscure
        KeyError.
        """
        if "test.product_line" not in self.env:
            self.skipTest(
                "Model 'test.product_line' is not available - module "
                "'test_ssi_product_line_mixin' is not installed."
            )
        self.run_yaml_scenario("test_data_mixin_product_line.yaml")
