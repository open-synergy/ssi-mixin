# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Related Attachment Mixin",
    "version": "11.0.1.0.0",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "wizards/attachment_related_attachment_import.xml",
        "views/attachment_related_attachment_category_views.xml",
        "views/attachment_related_attachment_template_detail_views.xml",
        "views/attachment_related_attachment_template_views.xml",
        "views/attachment_related_attachment.xml",
    ],
}
