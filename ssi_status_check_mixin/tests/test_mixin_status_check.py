# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMixinStatusCheck(YamlTransactionCase):
    """Scenario tests for ``mixin.status_check`` and ``status.check``.

    ``mixin.status_check`` is an ``AbstractModel`` and cannot be
    instantiated directly, so this suite runs it (and the concrete
    ``status.check`` model) through ``test_status_check_consumer``, a
    throwaway model declared in ``tests/fake_models.py`` and loaded via
    the ``fake_models:`` key of ``test_data_mixin_status_check.yaml`` -
    see that module's docstring for why it must not be imported here.
    """

    def test_mixin_status_check(self):
        """Run the status-check scenarios against the fake consumer model."""
        self.run_yaml_scenario("test_data_mixin_status_check.yaml")
