# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Test Module: Multiple Approval Mixin",
    "version": "11.0.1.1.0",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "mail",
        "ssi_multiple_approval_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/test_multiple_approval_view.xml",
    ],
}
