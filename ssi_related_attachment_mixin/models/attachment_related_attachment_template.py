# -*- coding: utf-8 -*-
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, fields, models


class AttachmentRelatedAttachmentTemplate(models.Model):
    _name = "attachment.related_attachment_template"
    _description = "Related Attachment Template"
    _order = "sequence asc, id"

    @api.model
    def _default_company_id(self):
        return self.env["res.company"]._company_default_get(self._name)

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
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="attachment.related_attachment_template_detail",
        inverse_name="template_id",
        copy=True,
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

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "[{}] {}".format(record.model, record.name)
            result.append((record.id, name))
        return result
