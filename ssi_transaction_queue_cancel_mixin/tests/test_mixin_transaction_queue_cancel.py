# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMixinTransactionQueueCancel(YamlTransactionCase):
    """Test the field definitions of the queue to cancel mixin."""

    def test_mixin_transaction_queue_cancel(self):
        """Run the field storage scenarios of the queue to cancel mixin."""
        self.run_yaml_scenario("test_data_mixin_transaction_queue_cancel.yaml")
