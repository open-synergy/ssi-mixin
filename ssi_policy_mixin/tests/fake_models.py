# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Throwaway models exercising ``mixin.policy`` for the unit test suite.

DELIBERATELY NOT IMPORTED FROM ``tests/__init__.py``, and not imported at
the top of ``tests/test_mixin_policy.py`` either. Odoo builds every model
class it sees while an addon loads, so importing this module there would
turn ``test_policy``/``test_policy_type`` into real models with real
tables in every database that installs ``ssi_policy_mixin``. The
``fake_models:`` key in ``tests/test_data_mixin_policy.yaml`` imports it
at the right moment instead, via
``odoo_yaml_test.YamlTransactionCase.run_yaml_scenario``.
"""

from odoo import api, fields, models


class TestPolicy(models.Model):
    """Concrete consumer of ``mixin.policy``, alive only in a test.

    ``mixin.policy`` is an ``AbstractModel`` and cannot be instantiated
    directly, so this fixture gives it a concrete model to run its
    template-selection, policy-evaluation and state-transition scenarios
    against.
    """

    _name = "test_policy"
    _description = "Test Policy"
    _inherit = [
        "mixin.policy",
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
            ("done", "Finished"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="test_policy_type",
    )
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    open_ok = fields.Boolean(
        string="Can Open",
        compute="_compute_policy",
    )
    done_ok = fields.Boolean(
        string="Can Finish",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        res += [
            "confirm_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "restart_ok",
        ]
        return res

    def _prepare_confirm_data(self):
        """Build the ``write()`` values for :meth:`action_confirm`.

        Extension point: override to add side-effect fields without
        touching :meth:`action_confirm` itself.

        :return: dict of values moving the record to ``confirm``
        """
        self.ensure_one()
        return {"state": "confirm"}

    def action_confirm(self):
        """Move every record in ``self`` to the ``confirm`` state."""
        for document in self:
            document.write(document._prepare_confirm_data())

    def _prepare_open_data(self):
        """Build the ``write()`` values for :meth:`action_open`.

        Extension point: override to add side-effect fields without
        touching :meth:`action_open` itself.

        :return: dict of values moving the record to ``open``
        """
        self.ensure_one()
        return {"state": "open"}

    def action_open(self):
        """Move every record in ``self`` to the ``open`` state."""
        for document in self:
            document.write(document._prepare_open_data())

    def _prepare_done_data(self):
        """Build the ``write()`` values for :meth:`action_done`.

        Extension point: override to add side-effect fields without
        touching :meth:`action_done` itself.

        :return: dict of values moving the record to ``done``
        """
        self.ensure_one()
        return {"state": "done"}

    def action_done(self):
        """Move every record in ``self`` to the ``done`` state."""
        for document in self:
            document.write(document._prepare_done_data())

    def _prepare_cancel_data(self):
        """Build the ``write()`` values for :meth:`action_cancel`.

        Extension point: override to add side-effect fields without
        touching :meth:`action_cancel` itself.

        :return: dict of values moving the record to ``cancel``
        """
        self.ensure_one()
        return {"state": "cancel"}

    def action_cancel(self):
        """Move every record in ``self`` to the ``cancel`` state."""
        for document in self:
            document.write(document._prepare_cancel_data())

    def _prepare_restart_data(self):
        """Build the ``write()`` values for :meth:`action_restart`.

        Extension point: override to add side-effect fields without
        touching :meth:`action_restart` itself.

        :return: dict of values moving the record back to ``draft``
        """
        self.ensure_one()
        return {"state": "draft"}

    def action_restart(self):
        """Move every record in ``self`` back to the ``draft`` state."""
        for document in self:
            document.write(document._prepare_restart_data())


class TestPolicyType(models.Model):
    """Unrelated model, alive only in a test.

    Carries no relationship to ``mixin.policy`` at all - used to prove
    that ``policy.template`` records are scoped to their own ``model``
    and never leak into an unrelated one (see the "allowed_policy_
    template_ids" scenario in ``test_data_mixin_policy.yaml``).
    """

    _name = "test_policy_type"
    _description = "Test Policy Type"

    name = fields.Char(
        string="# Document",
        required=True,
    )
