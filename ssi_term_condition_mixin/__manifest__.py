# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Terms and Conditions Mixin",
    "version": "19.0.1.0.0",
    "website": "https://github.com/open-synergy/ssi-mixin",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "templates/tnc_templates.xml",
        "views/tnc_section_views.xml",
        "views/tnc_clause_views.xml",
        "views/tnc_template_section_views.xml",
        "views/tnc_template_clause_views.xml",
        "views/tnc_template_views.xml",
    ],
    "demo": [],
}
