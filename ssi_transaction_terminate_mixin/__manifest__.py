# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Transaction Mixin - Terminate State",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "ssi_transaction_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/base_select_terminate_reason_views.xml",
        "templates/mixin_transaction_terminate_templates.xml",
        "views/ir_model_views.xml",
        "views/base_terminate_reason_views.xml",
    ],
    "demo": [
        "demo/base_terminate_reason_demo.xml",
    ],
}