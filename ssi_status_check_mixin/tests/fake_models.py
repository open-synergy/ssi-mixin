# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Throwaway model exercising ``mixin.status_check`` and the concrete
``status.check`` model for the unit test suite.

DELIBERATELY NOT IMPORTED FROM ``tests/__init__.py``, and not imported at
the top of ``tests/test_mixin_status_check.py`` either. Odoo builds every
model class it sees while an addon loads, so importing this module there
would turn ``test_status_check_consumer`` into a real model with a real
table in every database that installs ``ssi_status_check_mixin``. The
``fake_models:`` key in ``tests/test_data_mixin_status_check.yaml`` imports
it at the right moment instead, via
``odoo_yaml_test.YamlTransactionCase.run_yaml_scenario``.
"""

from odoo import fields, models


class TestStatusCheckConsumer(models.Model):
    """Consumer of ``mixin.status_check`` only, alive only in a test.

    Stands in for the permanent fixture model this module's tests used to
    bundle as real production code - a real table, real ACL row, and an
    unconditional import in ``models/__init__.py`` shipped to every
    database that installed this module (removed in favor of this
    throwaway class). Kept intentionally minimal: only ``name`` and
    ``state`` are declared, since none of the existing scenarios exercise
    log fields, ``partner_id``/``user_id``, the ``action_*`` methods, the
    onchange, or the ``unlink()``/``_compute_display_name`` overrides the
    old fixture carried, and ``mixin.status_check.create()`` already calls
    ``action_reload_status_check_template()`` on its own.
    """

    _name = "test_status_check_consumer"
    _description = "Test Status Check Consumer"
    _inherit = [
        "mixin.status_check",
    ]

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
        ],
        default="draft",
    )
