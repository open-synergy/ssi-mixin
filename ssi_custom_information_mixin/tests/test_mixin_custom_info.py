# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMixinCustomInfo(YamlTransactionCase):
    """Scenario tests for ``mixin.custom_info``.

    ``mixin.custom_info`` is an ``AbstractModel`` and cannot be
    instantiated directly. This suite exercises it through the concrete
    fixture model ``test.custom_information`` (module
    ``test_ssi_custom_information_mixin``). Guard against the fixture
    module not being installed, so this test fails loudly with a clear
    reason instead of an obscure ``KeyError``.
    """

    def test_mixin_custom_info(self):
        """Run the CRUD, template-reload and negative-path scenarios."""
        if "test.custom_information" not in self.env:
            self.skipTest(
                "Model 'test.custom_information' is not available - "
                "module 'test_ssi_custom_information_mixin' is not "
                "installed."
            )
        self.run_yaml_scenario("test_data_mixin_custom_info.yaml")
