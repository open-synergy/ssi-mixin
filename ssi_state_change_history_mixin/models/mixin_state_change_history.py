# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class MixinStateChangeHistory(models.AbstractModel):
    _name = "mixin.state_change_history"
    _description = "Mixin Object for State Change History"

    state_change_history_ids = fields.One2many(
        string="States Change History",
        comodel_name="state.change.history",
        inverse_name="res_id",
        domain=lambda self: [("model", "=", self._name)],
        auto_join=True,
    )

    @api.multi
    def _prepare_state_change_history(self, state_to):
        self.ensure_one()
        values = {
            "model": self._name,
            "res_id": self.id,
            "user_id": self.env.user.id,
            "state_from": self.state,
            "state_to": state_to,
            "date_change": fields.Datetime.now(),
        }
        return values

    @api.multi
    def create_state_change_history(self, state_to):
        self.ensure_one()
        obj_state_change_history = self.env["state.change.history"]
        obj_state_change_history.create(self._prepare_state_change_history(state_to))
        return True

    @api.multi
    def write(self, vals):
        for rec in self:
            if "state" in vals:
                rec.create_state_change_history(vals.get("state", False))
        return super(MixinStateChangeHistory, self).write(vals)
