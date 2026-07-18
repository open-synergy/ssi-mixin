# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Print Policy Mixin",
    "version": "19.0.1.0.0",
    "website": "https://github.com/open-synergy/ssi-mixin",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "base",
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/base_print_document.xml",
        "templates/mixin_print_templates.xml",
        "views/print_document_type_views.xml",
        "views/ir_actions_report_views.xml",
    ],
}
