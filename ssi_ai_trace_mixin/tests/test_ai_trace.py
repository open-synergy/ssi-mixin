# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAiTrace(YamlTransactionCase):
    """Cover the ``ai_trace`` model, its API, retention and access."""

    def test_ai_trace(self):
        """Run the ``ai_trace`` YAML scenarios against ``res.partner``."""
        self.run_yaml_scenario("test_data_ai_trace.yaml")

    def test_append_return_value(self):
        """Return the ids of ``ai_trace_append`` in the order of entries.

        Pure Python -- trigger P1 (L-01: ``action: call`` drops the
        return value of the method, so the ids cannot be asserted in
        YAML).
        """
        partner = self.env["res.partner"].create({"name": "AI Trace Partner"})
        entries = [
            {
                "model": "res.partner",
                "res_id": partner.id,
                "session_key": "order",
                "turn": turn,
                "kind": "turn",
                "prompt": "p%s" % turn,
            }
            for turn in (3, 1, 2)
        ]
        ids = self.env["ai_trace"].ai_trace_append(entries)
        records = self.env["ai_trace"].browse(ids)
        self.assertEqual(records.mapped("turn"), [3, 1, 2])
        again = self.env["ai_trace"].ai_trace_append(list(reversed(entries)))
        self.assertEqual(again, list(reversed(ids)))
