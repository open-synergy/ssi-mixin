# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MixinTransaction(models.AbstractModel):
    _name = "mixin.transaction"
    _inherit = [
        "mixin.sequence",
        "mail.thread",
        "mixin.policy",
    ]
    _description = "Transaction Mixin"
    _draft_state = "draft"
    _create_sequence_state = False

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
        copy=True,
    )
    note = fields.Text(
        string="Note",
        copy=True,
    )

    def _compute_policy(self):
        _super = super(MixinTransaction, self)
        _super._compute_policy()

    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )
    manual_number_ok = fields.Boolean(
        string="Can Input Manual Document Number",
        compute="_compute_policy",
    )

    def action_restart(self):
        for record in self:
            record.write(record._prepare_restart_data())

    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": self._draft_state,
        }

    def name_get(self):
        result = []
        for record in self:
            if record.name == "/":
                name = "*" + str(record.id)
            else:
                name = record.name
            result.append((record.id, name))
        return result

    def unlink(self):
        strWarning1 = _("You can only delete data on draft state")
        strWarning2 = _("You can only delete data without document number")
        force_unlink = self.env.context.get("force_unlink", False)
        for record in self:
            if record.state != "draft" and not force_unlink:
                raise UserError(strWarning1)
            if record.name != "/" and not force_unlink:
                raise UserError(strWarning2)
        _super = super(MixinTransaction, self)
        _super.unlink()
