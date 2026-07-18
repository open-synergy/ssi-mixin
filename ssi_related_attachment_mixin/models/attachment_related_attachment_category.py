# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AttachmentRelatedAttachmentCategory(models.Model):
    """
    Master-data model that groups related-attachment template details into
    named categories for display organisation on the attachment page.
    """

    _name = "attachment.related_attachment_category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Related Attachment Category"

    description = fields.Text(
        string="Description",
    )
