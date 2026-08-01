# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase
from psycopg2.errors import IntegrityError

from odoo.tests import tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestMixinMasterData(YamlTransactionCase):
    """Scenario tests for the ``mixin.master_data`` mixin.

    ``mixin.master_data`` is an ``AbstractModel`` and cannot be
    instantiated directly, so this suite exercises it through
    ``test_master_data``, a throwaway model declared in
    ``tests/fake_models.py`` and loaded via the ``fake_models:`` key of
    ``test_data_mixin_master_data.yaml`` - see that module's docstring
    for why it must not be imported here.
    """

    def test_mixin_master_data(self):
        """Run the CRUD, sequence and negative-path scenarios."""
        self.run_yaml_scenario("test_data_mixin_master_data.yaml")

    @mute_logger("odoo.sql_db")
    def test_create_without_name_is_rejected(self):
        """Reject creating a record without a ``name``.

        Pure Python - trigger P5 (L-22: the missing-required-value
        failure surfaces as ``psycopg2.errors.NotNullViolation``, a
        ``psycopg2.IntegrityError`` subtype outside the 12 error types
        ``expect_error`` understands). ``mute_logger("odoo.sql_db")``
        silences the PostgreSQL ERROR line this intentionally triggers,
        so ``oca_checklog_odoo`` does not fail the build.
        """
        self.run_yaml_scenario("test_data_mixin_master_data.yaml")
        with self.assertRaises(IntegrityError):
            self.env["test_master_data"].create({"code": "NO-NAME"})

    @mute_logger("odoo.sql_db")
    def test_create_without_code_is_rejected(self):
        """Reject creating a record without a ``code``.

        Pure Python - trigger P5 (L-22: the missing-required-value
        failure surfaces as ``psycopg2.errors.NotNullViolation``, a
        ``psycopg2.IntegrityError`` subtype outside the 12 error types
        ``expect_error`` understands). ``mute_logger("odoo.sql_db")``
        silences the PostgreSQL ERROR line this intentionally triggers,
        so ``oca_checklog_odoo`` does not fail the build.
        """
        self.run_yaml_scenario("test_data_mixin_master_data.yaml")
        with self.assertRaises(IntegrityError):
            self.env["test_master_data"].create({"name": "No Code"})
