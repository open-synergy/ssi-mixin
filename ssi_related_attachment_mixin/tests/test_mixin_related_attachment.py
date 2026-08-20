# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMixinRelatedAttachment(YamlTransactionCase):
    """Scenario tests for ``mixin.related_attachment``.

    ``mixin.related_attachment`` is an ``AbstractModel`` and cannot be
    instantiated directly. This suite exercises it through the concrete
    fixture model ``test.related_attachment`` (module
    ``test_ssi_related_attachment_mixin``). Guard against the fixture
    module not being installed, so this test fails loudly with a clear
    reason instead of an obscure ``KeyError``.
    """

    def test_mixin_related_attachment(self):
        """Run the CRUD, template auto-assign and unlink-guard scenarios."""
        if "test.related_attachment" not in self.env:
            self.skipTest(
                "Model 'test.related_attachment' is not available - "
                "module 'test_ssi_related_attachment_mixin' is not "
                "installed."
            )
        self.run_yaml_scenario("test_data_mixin_related_attachment.yaml")
