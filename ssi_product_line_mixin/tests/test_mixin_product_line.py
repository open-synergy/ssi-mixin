# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase
from psycopg2 import IntegrityError

from odoo.tests import tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestMixinProductLine(YamlTransactionCase):
    """Scenario tests for ``mixin.product_line``.

    ``mixin.product_line`` is an ``AbstractModel`` and cannot be
    instantiated directly. This suite exercises it through the concrete
    fixture model ``test.product_line`` (module
    ``test_ssi_product_line_mixin``). Guard against the fixture module not
    being installed, so this test fails loudly with a clear reason instead
    of an obscure ``KeyError``.
    """

    def _skip_if_fixture_missing(self):
        """Skip the running test when the fixture module is absent.

        :return: None
        """
        if "test.product_line" not in self.env:
            self.skipTest(
                "Model 'test.product_line' is not available - module "
                "'test_ssi_product_line_mixin' is not installed."
            )

    def test_mixin_product_line(self):
        """Run the CRUD, UoM and quantity conversion scenarios."""
        self._skip_if_fixture_missing()
        self.run_yaml_scenario("test_data_mixin_product_line.yaml")

    @mute_logger("odoo.sql_db")
    def test_name_is_required(self):
        """Reject creating a record without the required ``name``.

        Pure Python - trigger P5 (L-22: the NOT NULL violation raised for
        a missing required field surfaces as ``psycopg2.IntegrityError``,
        a type ``expect_error`` cannot recognise). ``name`` has no default,
        so simply omitting it reaches the database-level NOT NULL
        constraint.
        """
        self._skip_if_fixture_missing()
        with self.assertRaises(IntegrityError):
            self.env["test.product_line"].create({"uom_quantity": 1.0})
