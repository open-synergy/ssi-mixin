# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PrintDcoumentType(models.Model):
    """
    Represents a named *print document type* that groups related
    ``ir.actions.report`` records for a specific Odoo model.

    Each type defines which reports are available for a given model and
    provides the ``Print`` button drop-down list on the form view. Codes are
    generated via sequence and must be unique across all types.
    """

    _name = "print_document_type"
    _inherit = [
        "mail.activity.mixin",
        "mail.thread",
    ]
    _description = "Print Document Type"

    name = fields.Char(
        string="Type",
        required=True,
    )
    code = fields.Char(
        string="Code",
        default="/",
        required=True,
    )
    model_id = fields.Many2one(
        string="Referenced Model",
        comodel_name="ir.model",
        index=True,
        required=True,
        ondelete="cascade",
    )
    model = fields.Char(
        related="model_id.model",
        index=True,
        store=True,
    )
    report_ids = fields.Many2many(
        string="Reports",
        comodel_name="ir.actions.report",
        relation="rel_print_document_type_2_report",
        column1="type_id",
        column2="report_id",
        domain="[('model', '=', model)]",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )

    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        if "code" not in default:
            default["code"] = _("%s (copy)", self.code)
        return super().copy(default=default)

    @api.constrains("code")
    def _check_duplicate_code(self):
        for record in self:
            criteria = [
                ("code", "=", record.code),
                ("id", "!=", record.id),
                ("code", "!=", "/"),
            ]
            count_duplicate = self.search_count(criteria)
            if count_duplicate > 0:
                error_message = f"""
                Document Type: {self._description.lower()}
                Context: Create or update document
                Database ID: {self.id}
                Problem: Dupilicate code
                Solution: Change code
                """
                raise UserError(error_message)

    def action_generate_code(self):
        for record in self.sudo():
            record._create_sequence()

    def action_reset_code(self):
        for record in self.sudo():
            record.write(
                {
                    "code": "/",
                }
            )
