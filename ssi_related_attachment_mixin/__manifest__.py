# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Related Attachment Mixin",
    "version": "19.0.1.3.0",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_decorator",
        "ssi_master_data_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "templates/related_attachment_templates.xml",
        "wizards/attachment_related_attachment_import.xml",
        "views/ir_model_views.xml",
        "views/attachment_related_attachment_category_views.xml",
        "views/attachment_related_attachment_template_detail_views.xml",
        "views/attachment_related_attachment_template_views.xml",
        "views/attachment_related_attachment.xml",
    ],
}
