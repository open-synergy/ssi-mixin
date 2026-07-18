# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMixinStatusCheckGuard(YamlTransactionCase):
    def test_mixin_status_check_guard(self):
        # This module's ``mixin.status_check`` extension
        # (models/mixin_status_check.py) calls
        # ``onchange_state_change_constrain_template_id`` - a method that only
        # exists on models also inheriting "mixin.state_change_constrain". The
        # scenario proves the guard using both the "test.status_check" fixture
        # (mixin.status_check only, provided by the ssi_status_check_mixin
        # dependency) and the "test.state_change_constrain" fixture (both
        # mixins, bundled inside this module). Both models are loaded at
        # install, so no availability guard is needed.
        self.run_yaml_scenario("test_data_mixin_status_check_guard.yaml")
