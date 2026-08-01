# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Throwaway models exercising ``mixin.state_change_constrain`` and the
``mixin.status_check`` guard override for the unit test suite.

DELIBERATELY NOT IMPORTED FROM ``tests/__init__.py``, and not imported at
the top of ``tests/test_mixin_status_check_guard.py`` either. Odoo builds
every model class it sees while an addon loads, so importing this module
there would turn ``test_status_check_only_consumer``/
``test_state_change_consumer`` into real models with real tables in every
database that installs ``ssi_state_change_constrain_mixin``. The
``fake_models:`` key in ``tests/test_data_mixin_status_check_guard.yaml``
imports it at the right moment instead, via
``odoo_yaml_test.YamlTransactionCase.run_yaml_scenario``.
"""

from odoo import fields, models


class TestStatusCheckOnlyConsumer(models.Model):
    """Consumer of ``mixin.status_check`` only, alive only in a test.

    Stands in for the permanent fixture model this module's tests used to
    borrow from the ``ssi_status_check_mixin`` dependency (removed there in
    favor of its own throwaway model). Proves
    ``action_reload_status_check_template`` runs without ``AttributeError``
    on a model that never inherited ``mixin.state_change_constrain`` - the
    ``hasattr`` guard in ``models/mixin_status_check.py``.
    """

    _name = "test_status_check_only_consumer"
    _description = "Test Status Check Only Consumer"
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


class TestStateChangeConsumer(models.Model):
    """Consumer of both mixins, alive only in a test.

    ``mixin.state_change_constrain`` is an ``AbstractModel`` and cannot be
    instantiated directly, so this fixture gives it (and
    ``mixin.status_check``, which it needs for
    ``status_check_template_id``/``status_check_ids``) a concrete model to
    run the guard, template-selection and ``_check_state_constrain``
    scenarios against. ``state`` carries an extra ``open`` value, beyond
    the ``draft``/``confirm`` pair the mixin itself cares about, purely so
    a scenario can write to a state that no template detail binds and
    prove that path is left unblocked.
    """

    _name = "test_state_change_consumer"
    _description = "Test State Change Consumer"
    _inherit = [
        "mixin.state_change_constrain",
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
            ("open", "On Progress"),
        ],
        default="draft",
    )
