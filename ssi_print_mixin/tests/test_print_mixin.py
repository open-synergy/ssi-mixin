# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestPrintMixin(YamlTransactionCase):
    """Cover the print policy models of ``ssi_print_mixin``.

    All three models are concrete, so no fake model is needed:
    ``print_document_type``, ``ir.actions.report`` (print fields) and the
    ``base.print_document`` wizard. ``res.partner`` serves as the
    referenced model.
    """

    def _create_report(self, **values):
        """Create a ``res.partner`` report action.

        :param values: extra values merged over the defaults
        :return: the new ``ir.actions.report`` record
        """
        vals = {
            "name": "Test Print Report",
            "model": "res.partner",
            "report_type": "qweb-pdf",
            "report_name": "ssi_print_mixin.test_print_report",
        }
        vals.update(values)
        return self.env["ir.actions.report"].create(vals)

    def test_print_document_scenarios(self):
        """Run the YAML scenarios for the print policy models."""
        self.run_yaml_scenario("test_data_print_document.yaml")

    def test_copy_appends_copy_suffix_to_code(self):
        """Append ``(copy)`` to the code of a duplicated type.

        Pure Python - trigger P1 (L-01: ``action: call`` discards the
        record returned by ``copy()``).
        """
        model = self.env["ir.model"]._get("res.partner")
        document_type = self.env["print_document_type"].create(
            {
                "name": "Copy Source",
                "code": "PDT-COPY-SRC",
                "model_id": model.id,
            }
        )
        duplicate = document_type.copy()
        self.assertNotEqual(duplicate, document_type)
        self.assertEqual(duplicate.code, "PDT-COPY-SRC (copy)")

    def test_evaluate_print_python_code(self):
        """Evaluate the print condition to a boolean.

        Pure Python - trigger P1 (L-01: the boolean returned by
        ``_evaluate_print_python_code`` is discarded by ``action: call``).
        The default code yields ``True``, ``result = False`` yields
        ``False`` and code that raises yields ``False`` without error.
        """
        partner = self.env["res.partner"].create({"name": "Print Partner"})
        report = self._create_report()
        self.assertIs(report._evaluate_print_python_code(partner), True)
        report.print_python_code = "result = False"
        self.assertIs(report._evaluate_print_python_code(partner), False)
        report.print_python_code = "result = 1 / 0"
        self.assertIs(report._evaluate_print_python_code(partner), False)

    def test_action_print_returns_report_action(self):
        """Return a report action flagged to close the dialog.

        Pure Python - trigger P1 (L-01, L-02: the dict returned by
        ``action_print`` is discarded by ``action: call`` and cannot be
        asserted on).
        """
        partner = self.env["res.partner"].create({"name": "Print Partner"})
        report = self._create_report()
        wizard = (
            self.env["base.print_document"]
            .with_context(
                active_model="res.partner",
                active_ids=partner.ids,
                discard_logo_check=True,
            )
            .create({"report_action_id": report.id})
        )
        action = wizard.action_print()
        self.assertEqual(action["type"], "ir.actions.report")
        self.assertEqual(action["report_name"], report.report_name)
        self.assertIs(action["close_on_report_download"], True)
