# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Status Check",
    "version": "11.0.1.3.0",
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
        "views/status_check_item_views.xml",
        "views/status_check_template_detail_views.xml",
        "views/status_check_template_views.xml",
        "views/status_check_views.xml",
    ],
}
