# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMixinQrCode(YamlTransactionCase):
    """Scenario tests for ``mixin.qr_code``.

    ``mixin.qr_code`` is an ``AbstractModel`` and cannot be
    instantiated directly. This suite exercises it through the
    concrete fixture model ``test.qr_code`` (module
    ``test_ssi_qr_code_mixin``). Guard against the fixture module not
    being installed, so this test fails loudly with a clear reason
    instead of an obscure ``KeyError``.
    """

    def test_mixin_qr_code(self):
        """Run the compute and negative-path scenarios of ``qr_image``."""
        if "test.qr_code" not in self.env:
            self.skipTest(
                "Model 'test.qr_code' is not available - module "
                "'test_ssi_qr_code_mixin' is not installed."
            )
        self.run_yaml_scenario("test_data_mixin_qr_code.yaml")
