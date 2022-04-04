# -*- coding: utf-8 -*-
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, fields, models


class TestRelatedAttachment(models.Model):
    _name = "test.related_attachment"
    _description = "Test Related Attachment"
    _inherit = [
        "mixin.related_attachment",
        "mail.thread",
    ]

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
    )
    date = fields.Date(
        string="Date",
        index=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        copy=False,
        default=fields.Date.context_today,
    )
    user_id = fields.Many2one(
        string="Users",
        comodel_name="res.users",
        required=True,
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
            ("terminate", "Terminated"),
            ("reject", "Rejected"),
        ],
        default="draft",
    )

    @api.multi
    def action_confirm(self):
        for document in self:
            document.write({"state": "confirm"})

    @api.multi
    def action_open(self):
        for document in self:
            document.write({"state": "open"})

    @api.multi
    def action_done(self):
        for document in self:
            document.write({"state": "done"})

    @api.multi
    def action_cancel(self):
        for document in self:
            document.write({"state": "cancel"})

    @api.multi
    def action_restart(self):
        for document in self:
            document.write({"state": "draft"})

    @api.onchange(
        "user_id",
    )
    def onchange_related_attachment_template_id(self):
        super(TestRelatedAttachment, self)._onchange_related_attachment_template_id()
