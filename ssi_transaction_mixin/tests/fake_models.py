# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Throwaway consumer of ``mixin.transaction`` for the unit test suite.

DELIBERATELY NOT IMPORTED FROM ``tests/__init__.py`` NOR FROM THE TOP OF
``tests/test_mixin_transaction.py``. Odoo builds every model class that is
imported while the addon loads, so importing this module there would turn
``test_transaction_consumer`` into a real, permanent production model.
The ``fake_models:`` key in the YAML files imports it lazily instead, and
tears the model down again once the test method returns.
"""

from odoo import api, fields, models


class TestTransactionConsumer(models.Model):
    """Concrete consumer of ``mixin.transaction``, live only in a test.

    ``mixin.transaction`` is an ``AbstractModel`` and cannot be
    instantiated directly. This model gives it a concrete table so the
    numbering, protected deletion and restart rules can run through real
    ``create()`` / ``write()`` / ``unlink()`` calls.

    It adds a ``confirm`` state so ``action_restart`` has something to
    move back to ``draft``, and exposes the two policy flags the mixin
    declares (``restart_ok`` and ``manual_number_ok``). No policy template
    exists for this model, so both flags stay ``False`` unless a scenario
    passes the ``bypass_policy_check`` context.
    """

    _name = "test_transaction_consumer"
    _description = "Fake Transaction Consumer"
    _inherit = [
        "mixin.transaction",
    ]

    state = fields.Selection(
        selection_add=[
            ("confirm", "Confirmed"),
        ],
        ondelete={
            "confirm": "set default",
        },
    )

    @api.model
    def _get_policy_field(self):
        """Declare the policy flags this consumer computes.

        :return: list of policy field names, extended with the two flags
            owned by ``mixin.transaction``
        """
        res = super()._get_policy_field()
        res += [
            "restart_ok",
            "manual_number_ok",
        ]
        return res
