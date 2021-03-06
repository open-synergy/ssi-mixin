# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StatusCheckItem(models.Model):
    _name = "status.check.item"
    _description = "Status Check Item"

    name = fields.Char(
        string="Name",
        required=True,
    )
    code = fields.Char(
        string="Code",
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
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    description = fields.Text(
        string="Description",
    )
    status_check_method = fields.Selection(
        string="Status Check Method",
        selection=[
            ("use_python", "Python Code"),
        ],
        default="use_python",
        required=True,
    )
    python_code = fields.Text(
        string="Python Code",
        required=True,
        default="""# Available locals:\n#  - document: current record\nresult = True""",
    )
