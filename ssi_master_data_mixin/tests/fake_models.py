# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Throwaway model exercising ``mixin.master_data`` for the unit test suite.

DELIBERATELY NOT IMPORTED FROM ``tests/__init__.py``, and not imported at
the top of ``tests/test_mixin_master_data.py`` either. Odoo builds every
model class it sees while an addon loads, so importing this module there
would turn ``test_master_data`` into a real model with a real table in
every database that installs ``ssi_master_data_mixin``. The
``fake_models:`` key in ``tests/test_data_mixin_master_data.yaml`` imports
it at the right moment instead, via
``odoo_yaml_test.YamlTransactionCase.run_yaml_scenario``.
"""

from odoo import models


class TestMasterData(models.Model):
    """Concrete consumer of ``mixin.master_data``, alive only in a test.

    ``mixin.master_data`` is an ``AbstractModel`` and cannot be
    instantiated directly, so this fixture gives the mixin a concrete
    model to run its CRUD, sequence-generation, and duplicate-code
    scenarios against. No extra fields are declared - every field
    exercised by the test suite (``name``, ``code``, ``active``,
    ``note``) already comes from the mixin.
    """

    _name = "test_master_data"
    _description = "Test Master Data"
    _inherit = [
        "mixin.master_data",
    ]
