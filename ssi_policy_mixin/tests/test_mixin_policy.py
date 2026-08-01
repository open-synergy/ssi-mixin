# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMixinPolicy(YamlTransactionCase):
    """Scenario tests for the ``mixin.policy`` mixin.

    ``mixin.policy`` is an ``AbstractModel`` and cannot be instantiated
    directly, so this suite exercises it through ``test_policy`` and
    ``test_policy_type``, throwaway models declared in
    ``tests/fake_models.py`` and loaded via the ``fake_models:`` key of
    ``test_data_mixin_policy.yaml`` - see that module's docstring for why
    they must not be imported here.
    """

    def test_mixin_policy(self):
        """Run the template-selection and policy-evaluation scenarios."""
        self.run_yaml_scenario("test_data_mixin_policy.yaml")

    def test_get_template_policy_returns_false_without_match(self):
        """Return ``False`` when no ``policy.template`` matches.

        Pure Python - trigger P1 (L-01: the ``call`` action discards a
        method's return value, so YAML cannot assert directly on what
        ``_get_template_policy()`` returns when nothing matches).
        """
        self.run_yaml_scenario("test_data_mixin_policy.yaml")
        record = self.env["test_policy"].create({"name": "Unmatched Record"})
        self.assertFalse(record._get_template_policy())
