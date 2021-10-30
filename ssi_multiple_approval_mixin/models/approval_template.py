# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ApprovalTemplate(models.Model):
    _name = "approval.template"
    _description = "Approval Template"
    _order = "sequence"

    @api.model
    def _get_multiple_approval_model_names(self):
        res = []
        return res

    @api.model
    def _default_company_id(self):
        return self.env["res.company"]._company_default_get("approval.template")

    name = fields.Char(
        string="Name",
        required=True,
    )
    model_id = fields.Many2one(
        string="Referenced Model",
        comodel_name="ir.model",
        index=True,
        required=True,
    )
    model = fields.Char(
        related="model_id.model",
        index=True,
        store=True,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        default=lambda self: self._default_company_id(),
    )
    sequence = fields.Integer(
        default=1,
    )
    active = fields.Boolean(
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    validate_sequence = fields.Boolean(
        string="Validate by Sequence",
        help="Validation by reviewer must be done by sequence.",
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="approval.template_detail",
        inverse_name="template_id",
    )
    computation_method = fields.Selection(
        string="Computation Method",
        selection=[
            ("use_domain", "Domain"),
            ("use_python", "Python Code"),
        ],
        default="use_python",
        required=True,
    )
    domain = fields.Char(
        string="Domain",
    )
    python_code = fields.Text(
        string="Python Code",
        default="""# Available locals:\n#  - rec: current record""",
    )

    @api.onchange("model_id")
    def onchange_model_id(self):
        return {
            "domain": {
                "model_id": [("model", "in", self._get_multiple_approval_model_names())]
            }
        }
