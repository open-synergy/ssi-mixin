# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMixinDateDuration(YamlTransactionCase):
    """Scenario tests for ``mixin.date_duration``.

    ``mixin.date_duration`` is an ``AbstractModel`` and cannot be
    instantiated directly. This suite exercises it through the two
    concrete fixture models provided by module
    ``test_ssi_duration_mixin``: ``test.master_data_date_duration`` and
    ``test.transaction_date_duration``. Guard against the fixture module
    not being installed, so this test fails loudly with a clear reason
    instead of an obscure ``KeyError``.
    """

    def test_mixin_date_duration(self):
        """Run the CRUD and date-range negative-path scenarios."""
        if (
            "test.master_data_date_duration" not in self.env
            or "test.transaction_date_duration" not in self.env
        ):
            self.skipTest(
                "Models 'test.master_data_date_duration' / "
                "'test.transaction_date_duration' are not available - "
                "module 'test_ssi_duration_mixin' is not installed."
            )
        self.run_yaml_scenario("test_data_mixin_date_duration.yaml")
