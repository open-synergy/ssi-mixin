# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class StatusCheckTemplate(models.Model):
    _name = "status.check.template"
    _description = "Status Check Template"

    @api.model
    def _default_company_id(self):
        return self.env["res.company"]._company_default_get("status.check.template")

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
        string="Sequence",
        default=5,
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Notes",
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
        default="""# Available locals:\n#  - document: current record\nresult = True""",
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="status.check.template_detail",
        inverse_name="template_id",
    )
