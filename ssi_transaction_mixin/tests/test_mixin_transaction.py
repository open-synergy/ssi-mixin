# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMixinTransaction(YamlTransactionCase):
    """Cover ``mixin.transaction`` through a ``fake_models:``-only consumer.

    ``mixin.transaction`` is an ``AbstractModel``. It is exercised through
    ``tests.fake_models.TestTransactionConsumer``, a throwaway concrete
    model declared via ``fake_models:`` in the YAML files. It is never
    shipped to production and never imported at addon-load time.
    """

    def _load_consumer(self):
        """Register the fake consumer model through a minimal YAML file.

        The Python tests below need the fake model to exist, and the only
        supported way to load it is the ``fake_models:`` key of a YAML
        scenario file. The model is unloaded again when the test returns.
        """
        self.run_yaml_scenario("test_data_mixin_transaction_loader.yaml")
        # Cleanups run LIFO, so this flush runs before the library unloads
        # the fake model. Otherwise a pending ORM write on the fake model
        # makes the registry re-setup fail with KeyError at teardown.
        self.addCleanup(self.env.flush_all)

    def test_mixin_transaction(self):
        """Run the ``mixin.transaction`` YAML scenarios."""
        self.run_yaml_scenario("test_data_mixin_transaction.yaml")

    def test_display_name(self):
        """Check the display name of a document.

        Pure Python: P1, because the display name is the value computed by
        ``_compute_display_name`` and is built from the record id
        (``*<id>``), which an ``expected`` literal in YAML cannot express
        (L-01, L-09).
        """
        self._load_consumer()
        obj_consumer = self.env["test_transaction_consumer"]
        document = obj_consumer.create({})
        self.assertEqual(document.name, "/")
        self.assertEqual(document.display_name, f"*{document.id}")
        document.write({"name": "TX-DISPLAY-001"})
        self.assertEqual(document.display_name, "TX-DISPLAY-001")

    def test_check_duplicate_document_number(self):
        """Check the return value of ``_check_duplicate_document_number``.

        Pure Python: P1, because the method only returns ``True`` or
        ``False`` and ``action: call`` discards return values (L-01). A
        real duplicate is forced through SQL, since the constraint refuses
        to let ORM writes create one.
        """
        self._load_consumer()
        obj_consumer = self.env["test_transaction_consumer"]
        first = obj_consumer.create({"name": "TX-PYDUP-001"})
        second = obj_consumer.create({"name": "TX-PYDUP-002"})
        slash = obj_consumer.create({})
        other_slash = obj_consumer.create({})
        self.assertTrue(first._check_duplicate_document_number())
        self.assertTrue(second._check_duplicate_document_number())
        self.assertTrue(slash._check_duplicate_document_number())
        self.assertTrue(other_slash._check_duplicate_document_number())
        second.flush_recordset()
        self.env.cr.execute(
            "UPDATE test_transaction_consumer SET name = %s WHERE id = %s",
            ("TX-PYDUP-001", second.id),
        )
        second.invalidate_recordset(["name"])
        self.assertFalse(second._check_duplicate_document_number())
        self.assertFalse(first._check_duplicate_document_number())

    def test_check_unlink_helpers(self):
        """Check ``_check_state_unlink`` and ``_check_document_number_unlink``.

        Pure Python: P1, because both helpers only return ``True`` or
        ``False`` and ``action: call`` discards return values (L-01).
        """
        self._load_consumer()
        obj_consumer = self.env["test_transaction_consumer"]
        draft = obj_consumer.create({})
        self.assertTrue(draft._check_state_unlink())
        self.assertTrue(draft._check_document_number_unlink())
        confirmed = obj_consumer.create({})
        confirmed.write({"state": "confirm"})
        self.assertFalse(confirmed._check_state_unlink())
        self.assertTrue(confirmed._check_state_unlink(force_unlink=True))
        numbered = obj_consumer.create({"name": "TX-PYUNL-001"})
        self.assertFalse(numbered._check_document_number_unlink())
        self.assertTrue(numbered._check_document_number_unlink(force_unlink=True))

    def test_unlink_returns_true(self):
        """Check that ``unlink`` returns the result of ``super().unlink()``.

        Pure Python: P1, because ``action: unlink`` discards the return
        value (L-01).
        """
        self._load_consumer()
        obj_consumer = self.env["test_transaction_consumer"]
        draft = obj_consumer.create({})
        self.assertTrue(draft.unlink())
