# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AttachmentRelatedAttachmentTemplateDetail(models.Model):
    _name = "attachment.related_attachment_template_detail"
    _description = "Related Attachment Template Detail"

    template_id = fields.Many2one(
        string="# Template",
        comodel_name="attachment.related_attachment_template",
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        related="template_id.company_id",
        store=True,
    )
    sequence = fields.Integer(
        default=1,
    )
    active = fields.Boolean(
        default=True,
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="attachment.related_attachment_category",
        required=True,
    )
    verify_method = fields.Selection(
        string="Verify Method",
        selection=[
            ("use_user", "Users"),
            ("use_group", "Groups"),
            ("use_both", "Both specific user and group."),
            ("use_python", "Python Code"),
        ],
        default="use_user",
        required=True,
    )
    verify_user_ids = fields.Many2many(
        string="Users",
        comodel_name="res.users",
        relation="rel_related_attachment_template_detail_2_user",
        column1="detail_id",
        column2="user_id",
    )
    verify_group_ids = fields.Many2many(
        string="Groups",
        comodel_name="res.groups",
        relation="rel_related_attachment_template_detail_2_group",
        column1="detail_id",
        column2="group_id",
    )
    python_code = fields.Text(
        string="Python Code",
        default="""# Available locals:\n#  - rec: current record""",
    )
