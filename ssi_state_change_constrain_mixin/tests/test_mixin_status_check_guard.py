# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMixinStatusCheckGuard(YamlTransactionCase):
    def test_mixin_status_check_guard(self):
        # This module's ``mixin.status_check`` extension (models/mixin_status_check.py)
        # calls ``onchange_state_change_constrain_template_id`` - a method that only
        # exists on models also inheriting "mixin.state_change_constrain". The scenario
        # relies on "test.status_check" (module "test_ssi_status_check_mixin", a mixin
        # -status_check-only model) being installed to prove the guard; skip loudly if
        # it is not, instead of an obscure KeyError.
        if "test.status_check" not in self.env:
            self.skipTest(
                "Model 'test.status_check' is not available - module "
                "'test_ssi_status_check_mixin' is not installed."
            )
        self.run_yaml_scenario("test_data_mixin_status_check_guard.yaml")
