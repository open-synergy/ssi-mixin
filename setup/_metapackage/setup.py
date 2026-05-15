import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-open-synergy-ssi-mixin",
    description="Meta package for open-synergy-ssi-mixin Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-ssi_company_currency_mixin',
        'odoo11-addon-ssi_custom_information_mixin',
        'odoo11-addon-ssi_master_data_mixin',
        'odoo11-addon-ssi_multiple_approval_mixin',
        'odoo11-addon-ssi_policy_mixin',
        'odoo11-addon-ssi_product_line_mixin',
        'odoo11-addon-ssi_product_line_price_mixin',
        'odoo11-addon-ssi_related_attachment_mixin',
        'odoo11-addon-ssi_sequence_mixin',
        'odoo11-addon-ssi_source_document_mixin',
        'odoo11-addon-ssi_state_change_constrain_mixin',
        'odoo11-addon-ssi_state_change_history_mixin',
        'odoo11-addon-ssi_status_check_mixin',
        'odoo11-addon-ssi_transaction_cancel_mixin',
        'odoo11-addon-ssi_transaction_confirm_mixin',
        'odoo11-addon-ssi_transaction_done_mixin',
        'odoo11-addon-ssi_transaction_mixin',
        'odoo11-addon-ssi_transaction_open_mixin',
        'odoo11-addon-ssi_transaction_terminate_mixin',
        'odoo11-addon-test_multiple_approval_mixin',
        'odoo11-addon-test_ssi_custom_information_mixin',
        'odoo11-addon-test_ssi_policy_mixin',
        'odoo11-addon-test_ssi_related_attachment_mixin',
        'odoo11-addon-test_ssi_sequence_mixin',
        'odoo11-addon-test_ssi_state_change_constrain_mixin',
        'odoo11-addon-test_ssi_state_change_history_mixin',
        'odoo11-addon-test_ssi_transaction_mixin',
        'odoo11-addon-test_status_check_mixin',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 11.0',
    ]
)
