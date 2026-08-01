# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMixinSequence(YamlTransactionCase):
    """Cover ``mixin.sequence`` through a ``fake_models:``-only consumer.

    ``mixin.sequence`` is an ``AbstractModel`` and cannot be instantiated
    directly. This suite exercises it through
    ``tests.fake_models.TestSequenceConsumer``, a throwaway concrete model
    declared by ``test_data_mixin_sequence.yaml`` via ``fake_models:`` — it
    is never shipped to production and never imported at addon-load time.
    """

    def test_mixin_sequence(self):
        """Run the ``mixin.sequence`` YAML scenarios."""
        self.run_yaml_scenario("test_data_mixin_sequence.yaml")
