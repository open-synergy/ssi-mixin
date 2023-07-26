# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class TestAccountMoveOneMixin(models.Model):
    _name = "test.account_move_one_mixin"
    _description = "Test Account Move One Mixin"
    _inherit = [
        "mixin.account_move",
        "mixin.currency",
        "mixin.company_currency",
        "mixin.account_move_single_line",
    ]
    _exchange_date_field = "date"
    _journal_id_field_name = "journal_id"
    _move_id_field_name = "move_id"
    _accounting_date_field_name = "date"
    _currency_id_field_name = "currency_id"
    _company_currency_id_field_name = "company_currency_id"

    _account_id_field_name = "account_id"
    _partner_id_field_name = "partner_id"
    _analytic_account_id_field_name = False
    _amount_currency_field_name = "amount_total"
    _date_field_name = "date"
    _label_field_name = "name"
    _date_due_field_name = "date_due"

    _need_date_due = True
    _normal_amount = "debit"

    # Tax computation
    _tax_lines_field_name = "tax_ids"
    _tax_on_self = False
    _tax_source_recordset_field_name = "detail_ids"
    _price_unit_field_name = "amount"
    _quantity_field_name = False

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
    )
    date = fields.Date(
        string="Date",
        default=fields.Date.context_today,
        required=True,
    )
    date_due = fields.Date(
        string="Date Due",
        default=fields.Date.context_today,
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=True,
    )
    move_id = fields.Many2one(
        string="# Move",
        comodel_name="account.move",
        readonly=True,
    )
    detail_ids = fields.One2many(
        comodel_name="test.account_move_line_one_mixin",
        inverse_name="header_object_id",
    )
    amount_total = fields.Monetary(
        currency_field="currency_id",
        compute="_compute_amount",
        store=True,
    )
    amount_tax = fields.Monetary(
        currency_field="currency_id",
        compute="_compute_amount",
        store=True,
    )
    amount_untaxed = fields.Monetary(
        currency_field="currency_id",
        compute="_compute_amount",
        store=True,
    )
    tax_ids = fields.One2many(
        comodel_name="test.tax_line_one_mixin",
        inverse_name="header_object_id",
    )

    @api.depends(
        "detail_ids",
        "detail_ids.amount",
    )
    def _compute_amount(self):
        for record in self:
            record.amount_total = record.amount_tax = record.amount_untaxed = 0.0
            for detail in record.detail_ids:
                record.amount_untaxed += detail.amount
            for tax in record.tax_ids:
                record.amount_tax += tax.tax_amount
            record.amount_total = record.amount_untaxed + record.amount_tax

    def action_create_accounting_entry(self):
        for record in self.sudo():
            record._create_standard_move()
            record._create_standard_ml()
            for detail in record.detail_ids:
                detail._create_standard_ml()
            for tax in record.tax_ids:
                tax._create_standard_ml()

    def action_delete_accounting_entry(self):
        for record in self.sudo():
            record._delete_standard_move()

    def action_compute_tax(self):
        for record in self.sudo():
            record._recompute_standard_tax()


class TestAccountMoveLineOneMixin(models.Model):
    _name = "test.account_move_line_one_mixin"
    _description = "Test Account Move Line One Mixin"
    _inherit = [
        "mixin.account_move_single_line",
    ]

    _move_id_field_name = "move_id"
    _account_id_field_name = "account_id"
    _partner_id_field_name = False
    _analytic_account_id_field_name = "analytic_account_id"
    _currency_id_field_name = "currency_id"
    _company_currency_id_field_name = "company_currency_id"
    _amount_currency_field_name = "amount"
    _company_id_field_name = "company_id"
    _date_field_name = "date"
    _label_field_name = "name"

    _normal_amount = "credit"

    header_object_id = fields.Many2one(
        comodel_name="test.account_move_one_mixin",
        required=True,
        ondelete="cascade",
    )
    account_id = fields.Many2one(
        comodel_name="account.account",
        required=True,
        ondelete="restrict",
    )
    name = fields.Char(
        required=True,
    )
    amount = fields.Monetary(
        currency_field="currency_id",
    )
    currency_id = fields.Many2one(
        related="header_object_id.currency_id",
    )
    company_currency_id = fields.Many2one(
        related="header_object_id.company_currency_id",
    )
    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
    )
    company_id = fields.Many2one(
        related="header_object_id.company_id",
    )
    move_id = fields.Many2one(
        related="header_object_id.move_id",
    )
    date = fields.Date(
        related="header_object_id.date",
    )
    tax_ids = fields.Many2many(
        comodel_name="account.tax",
    )


class TestTaxLineOneMixin(models.Model):
    _name = "test.tax_line_one_mixin"
    _description = "Test Tax One Mixin"
    _inherit = [
        "mixin.tax_line",
    ]

    _move_id_field_name = "move_id"
    _account_id_field_name = "account_id"
    _partner_id_field_name = "partner_id"
    _analytic_account_id_field_name = "analytic_account_id"
    _currency_id_field_name = "currency_id"
    _company_currency_id_field_name = "company_currency_id"
    _amount_currency_field_name = "tax_amount"
    _company_id_field_name = "company_id"
    _date_field_name = "date"
    _label_field_name = "name"

    _normal_amount = "credit"

    header_object_id = fields.Many2one(
        comodel_name="test.account_move_one_mixin",
        required=True,
        ondelete="cascade",
    )
    currency_id = fields.Many2one(
        related="header_object_id.currency_id",
    )
    company_currency_id = fields.Many2one(
        related="header_object_id.company_currency_id",
    )
    company_id = fields.Many2one(
        related="header_object_id.company_id",
    )
    move_id = fields.Many2one(
        related="header_object_id.move_id",
    )
    date = fields.Date(
        related="header_object_id.date",
    )
    partner_id = fields.Many2one(
        related="header_object_id.partner_id",
    )
