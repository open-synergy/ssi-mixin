# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMixinStatusCheckGuard(YamlTransactionCase):
    """Scenario tests for the ``mixin.status_check`` guard override and
    ``mixin.state_change_constrain`` itself.

    This module's ``mixin.status_check`` extension
    (``models/mixin_status_check.py``) calls
    ``onchange_state_change_constrain_template_id`` - a method that only
    exists on models also inheriting ``mixin.state_change_constrain``. Both
    mixins, and the concrete models needed to exercise them, have no
    standalone implementation of their own, so this suite runs them through
    ``test_status_check_only_consumer`` and ``test_state_change_consumer``,
    throwaway models declared in ``tests/fake_models.py`` and loaded via the
    ``fake_models:`` key of ``test_data_mixin_status_check_guard.yaml`` -
    see that module's docstring for why they must not be imported here.
    """

    def test_mixin_status_check_guard(self):
        """Run the guard, template-selection and state-constrain scenarios."""
        self.run_yaml_scenario("test_data_mixin_status_check_guard.yaml")
