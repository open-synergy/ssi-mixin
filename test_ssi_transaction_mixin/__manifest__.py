# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Test Module: Transaction Mixin",
    "version": "14.0.1.1.0",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_transaction_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_open_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_transaction_terminate_mixin",
        "ssi_product_line_price_mixin",
        "ssi_company_currency_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/sequence_template_data.xml",
        "data/policy_template_data.xml",
        "data/approval_template_data.xml",
        "views/test_transaction_mixin_view.xml",
        "views/test_transaction_mixin_inherit_view.xml",
    ],
}
