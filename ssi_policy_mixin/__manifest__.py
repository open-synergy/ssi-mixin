# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Policy Mixin",
    "version": "11.0.1.1.0",
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
        "views/policy_template_views.xml",
        "views/policy_template_detail_views.xml",
    ],
}
