# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MixinStatusCheck(models.AbstractModel):
    """
    Extends ``mixin.status_check`` from ``ssi_status_check_mixin`` to reload
    the state-change constrain template alongside the status-check template
    when ``action_reload_status_check_template`` is triggered.

    Not every model that uses ``mixin.status_check`` also uses
    ``mixin.state_change_constrain`` (e.g. ``ssi_status_check_mixin``'s own
    test fixture, or this module's own ``test_status_check_only_consumer``).
    The ``hasattr`` guard below keeps this override safe for those models
    instead of raising ``AttributeError`` on every ``create()``.
    """

    _inherit = "mixin.status_check"

    def action_reload_status_check_template(self):
        _super = super()
        _super.action_reload_status_check_template()
        for record in self:
            if hasattr(record, "onchange_state_change_constrain_template_id"):
                record.onchange_state_change_constrain_template_id()
