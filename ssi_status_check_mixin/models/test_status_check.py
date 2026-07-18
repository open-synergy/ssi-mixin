# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class TestStatusCheck(models.Model):
    """Concrete fixture model that inherits ``mixin.status_check`` so the
    abstract mixin (and the concrete ``status.check`` model) can be exercised
    by the in-module test suite. It is bundled inside this module (loaded at
    install) so the mixin is self-testing. ``mail.thread`` is intentionally
    dropped: this module does not depend on ``mail`` and no test scenario
    relies on chatter/message_post."""

    _name = "test.status_check"
    _description = "Test Status Check"
    _inherit = [
        "mixin.status_check",
    ]
    _order = "id"

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
    )
    user_id = fields.Many2one(
        string="User",
        comodel_name="res.users",
    )
    date = fields.Date(
        string="Date",
        index=True,
        readonly=True,
        copy=False,
        default=fields.Date.context_today,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    notes = fields.Text(
        string="Notes",
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

    # Log Fields
    confirm_date = fields.Datetime(
        string="Confirm Date",
        readonly=True,
        copy=False,
    )
    confirm_user_id = fields.Many2one(
        string="Confirmed By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    open_date = fields.Datetime(
        string="Open Date",
        readonly=True,
        copy=False,
    )
    open_user_id = fields.Many2one(
        string="Opened By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    done_date = fields.Datetime(
        string="Finish Date",
        readonly=True,
        copy=False,
    )
    done_user_id = fields.Many2one(
        string="Finished By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    cancel_date = fields.Datetime(
        string="Cancel Date",
        readonly=True,
        copy=False,
    )
    cancel_user_id = fields.Many2one(
        string="Cancelled By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )

    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
            "confirm_date": fields.Datetime.now(),
            "confirm_user_id": self.env.user.id,
        }

    def action_confirm(self):
        for document in self:
            document.write(document._prepare_confirm_data())

    def _prepare_open_data(self):
        self.ensure_one()
        return {
            "state": "open",
            "open_date": fields.Datetime.now(),
            "open_user_id": self.env.user.id,
        }

    def action_open(self):
        for document in self:
            document.write(document._prepare_open_data())

    def _prepare_done_data(self):
        self.ensure_one()
        return {
            "state": "done",
            "done_date": fields.Datetime.now(),
            "done_user_id": self.env.user.id,
        }

    def action_done(self):
        for document in self:
            document.write(document._prepare_done_data())

    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
        }

    def action_cancel(self):
        for document in self:
            document.write(document._prepare_cancel_data())

    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "open_date": False,
            "open_user_id": False,
            "done_date": False,
            "done_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
        }

    def action_restart(self):
        for document in self:
            document.write(document._prepare_restart_data())

    @api.onchange(
        "user_id",
    )
    def onchange_status_check_template_id(self):
        self.status_check_template_id = False
        if self.user_id:
            template_id = self._get_template_status_check()
            self.status_check_template_id = template_id

    @api.model_create_multi
    def create(self, vals_list):
        _super = super()
        results = _super.create(vals_list)
        for result in results:
            template_id = result._get_template_status_check()
            if template_id:
                result.write(
                    {
                        "status_check_template_id": template_id,
                    }
                )
                result.create_status_check_ids()
        return results

    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        force_unlink = self.env.context.get("force_unlink", False)
        for record in self:
            if record.state != "draft" and not force_unlink:
                raise UserError(strWarning)
        _super = super()
        _super.unlink()

    @api.depends("name")
    def _compute_display_name(self):
        for record in self:
            if record.name == "/":
                record.display_name = "*" + str(record.id)
            else:
                record.display_name = record.name
