# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Throwaway model that exercises ``mixin.sequence`` for the fake-model test.

DELIBERATELY NOT IMPORTED FROM ``tests/__init__.py`` NOR FROM THE TOP OF ANY
TEST MODULE. Odoo builds every model class that is imported while the addon
loads, so importing this module at load time would turn
``test_sequence_consumer`` into a real, permanent production model —
exactly the fixture leak this refactor removes. The ``fake_models`` key in
``test_data_mixin_sequence.yaml`` imports this module lazily, after the
test registry has been snapshotted, and tears the model down again through
``addCleanup`` once the test method returns.
"""

from odoo import api, fields, models


class TestSequenceConsumer(models.Model):
    """Concrete consumer of ``mixin.sequence``, live only during the test.

    Exists solely so ``tests/test_data_mixin_sequence.yaml`` can exercise
    the abstract mixin's ``_create_sequence`` / ``_evaluate_sequence``
    methods through a real ``create()`` call. Mirrors the fields and the
    ``create()`` override that used to live in the permanent database
    fixture model this refactor deletes; this is not a rename of that
    model, just a replacement for the same role.
    """

    _name = "test_sequence_consumer"
    _description = "Fake Consumer Of Mixin Sequence"
    _inherit = [
        "mixin.sequence",
    ]

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
    )
    date = fields.Date(
        string="Date",
        default=fields.Date.context_today,
    )
    notes = fields.Text(
        string="Notes",
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Create records, then run ``_create_sequence`` on each of them.

        This is the production entry point that drives
        ``mixin.sequence._evaluate_sequence`` /
        ``_evaluate_sequence_use_python`` /
        ``_evaluate_sequence_use_domain`` for every scenario declared in
        ``test_data_mixin_sequence.yaml``.

        :param vals_list: list of value dicts for the new records
        :return: the newly created recordset
        """
        records = super().create(vals_list)
        for record in records:
            record._create_sequence()
        return records
