# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class StateChangeConstrainTemplate(models.Model):
    _name = "state.change.constrain.template"
    _description = "State Change Constrain Template"

    @api.model
    def _default_company_id(self):
        return self.env["res.company"]._company_default_get(
            "state.change.constrain.template"
        )

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
    status_check_template_id = fields.Many2one(
        string="Status Check Template",
        comodel_name="status.check.template",
        index=True,
        required=True,
    )

    @api.multi
    @api.depends("status_check_template_id")
    def _compute_allowed_check_item_ids(self):
        obj_status_check_template = self.env["status.check.template"]
        item_ids = []
        for document in self:
            if document.status_check_template_id:
                template_id = obj_status_check_template.search(
                    [("id", "=", document.status_check_template_id.id)]
                )
                if template_id:
                    item_ids = template_id.mapped("detail_ids").mapped(
                        "status_check_item_id"
                    )
            document.allowed_check_item_ids = item_ids

    allowed_check_item_ids = fields.Many2many(
        string="Allowed Check Items",
        comodel_name="status.check.item",
        compute="_compute_allowed_check_item_ids",
        store=False,
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
        comodel_name="state.change.constrain.template_detail",
        inverse_name="template_id",
    )
