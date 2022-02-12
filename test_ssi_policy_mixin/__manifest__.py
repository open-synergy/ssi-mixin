# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Test Module: Policy Mixin",
    "version": "11.0.1.2.0",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "mail",
        "ssi_policy_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/test_policy_type_view.xml",
        "views/test_policy_view.xml",
    ],
}
