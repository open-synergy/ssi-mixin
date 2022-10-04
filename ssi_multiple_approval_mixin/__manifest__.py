# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Multiple Approval Mixin",
    "version": "11.0.1.5.1",
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
        "templates/mixin_multiple_approval_templates.xml",
        "menu.xml",
        "views/approval_template_detail_views.xml",
        "views/approval_template_views.xml",
        "views/approval_approval_views.xml",
    ],
}
