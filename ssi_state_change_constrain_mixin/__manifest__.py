# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "State Change Constrain Mixin",
    "version": "14.0.1.0.0",
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
