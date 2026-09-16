# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMixinProductLineAccount(YamlTransactionCase):
    """Cover ``mixin.product_line_account._compute_total()``.

    ``mixin.product_line_account`` is an AbstractModel and cannot be
    instantiated directly, so this suite exercises it through the
    concrete fixture model ``test.product_line_account`` (module
    ``test_ssi_product_line_account_mixin``).
    """

    def test_mixin_product_line_account(self):
        """Run the ``_compute_total`` rounding-vs-tax scenarios.

        Guard against the fixture module not being installed, so this
        test fails loudly with a clear reason instead of an obscure
        KeyError.
        """
        if "test.product_line_account" not in self.env:
            self.skipTest(
                "Model 'test.product_line_account' is not available - "
                "module 'test_ssi_product_line_account_mixin' is not "
                "installed."
            )
        self.run_yaml_scenario("test_data_mixin_product_line_account.yaml")
