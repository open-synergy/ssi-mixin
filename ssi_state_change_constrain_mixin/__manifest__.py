# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "State Change Constrain Mixin",
    "version": "11.0.1.3.0",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "ssi_status_check_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "views/state_change_constrain_template_views.xml",
    ],
}
