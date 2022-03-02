# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Test Module: Multiple Approval Mixin",
    "version": "14.0.1.0.0",
    "category": "Administration",
    "website": "https://github.com/OCA/vertical-rental",
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