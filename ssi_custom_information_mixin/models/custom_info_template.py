# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CustomInfoTemplate(models.Model):
    _description = "Custom information template"
    _name = "custom_info.template"
    _order = "model_id, name"

    name = fields.Char(required=True, translate=True)
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

    @api.model
    def _default_company_id(self):
        return self.env["res.company"]._company_default_get("approval.template")

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        default=lambda self: self._default_company_id(),
    )
    sequence = fields.Integer(
        default=1,
        required=True,
    )
    active = fields.Boolean(
        default=True,
    )
    note = fields.Text(
        string="Note",
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
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="custom_info.template_detail",
        inverse_name="template_id",
    )
