[![Build Status](https://travis-ci.com/open-synergy/ssi-mixin.svg?branch=14.0)](https://travis-ci.com/open-synergy/ssi-mixin)
![pre-commit](https://github.com/open-synergy/ssi-mixin/actions/workflows/pre-commit.yml/badge.svg)
[![codecov](https://codecov.io/gh/open-synergy/ssi-mixin/branch/14.0/graph/badge.svg)](https://codecov.io/gh/open-synergy/ssi-mixin)

<!-- /!\ do not modify above this line -->

# ssi-mixin

ssi-mixin

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Technical Addons
----------------
addon | summary
--- | ---
[ssi_decorator](ssi_decorator/) | Menambahkan decorator pre/post check atau action untuk setiap workflow state
[ssi_partner_mixin](ssi_partner_mixin/) | Menambahkan field partner dan contact partner
[ssi_salesperson_mixin](ssi_salesperson_mixin/) | Menambahkan field salesperson dan sales team
[ssi_company_currency_mixin](ssi_company_currency_mixin/) | Menambahkan field company dan company currency
[ssi_duration_mixin](ssi_duration_mixin/) | Menambahkan field date start dan date end
[ssi_field_date_callable_attribute](ssi_field_date_callable_attribute/) | Base module untuk field date
[ssi_pricelist_mixin](ssi_pricelist_mixin/) | Menambahkan field currency dan pricelist
[ssi_product_line_mixin](ssi_product_line_mixin/) | Menambahkan product line tanpa pricelist
[ssi_product_line_price_mixin](ssi_product_line_price_mixin/) | Menambahkan product line dengan pricelist
[ssi_product_line_account_mixin](ssi_product_line_account_mixin/) | Menambahkan field-field accounting pada product line
[ssi_source_document_mixin](ssi_source_document_mixin/)| Menambahkan field source document
[ssi_master_data_mixin](ssi_master_data_mixin/) | Base module untuk pembuatan objek master data

Functional Addons
-----------------
addon | summary
--- | ---
[ssi_custom_information_mixin](ssi_custom_information_mixin/) | Menambahkan fungsionalitas untuk custom information
[ssi_multiple_approval_mixin](ssi_multiple_approval_mixin/) | Menambahkan fungsionalitas untuk multiple approval
[ssi_operating_unit_mixin](ssi_operating_unit_mixin/) | Menambahkan fungsionalitas untuk operating unit
[ssi_policy_mixin](ssi_policy_mixin/) | Menambahkan fungsionalitas untuk workflow policy
[ssi_print_mixin](ssi_print_mixin/) | Menambahkan fungsionalitas untuk proses percetakan dokument
[ssi_qr_code_mixin](ssi_qr_code_mixin/) | Menambahkan fungsionalitas untuk QR Code
[ssi_related_attachment_mixin](ssi_related_attachment_mixin/) | Menambahkan fungsionalitas untuk related attachment
[ssi_sequence_mixin](ssi_sequence_mixin/) | Menambahkan fungsionalitas untuk sequence
[ssi_state_change_constrain_mixin](ssi_state_change_constrain_mixin/) | Menambahkan fungsionalitas untuk state change constrain
[ssi_status_check_mixin](ssi_status_check_mixin/) | Menambahkan fungsionalitas untuk status check
[ssi_transaction_mixin](ssi_transaction_mixin/) | Base module untuk pembuatan objek transaksi
[ssi_transaction_confirm_mixin](ssi_transaction_confirm_mixin/) | Menambahkan proses workflow state confim pada objek transaksi
[ssi_transaction_done_mixin](ssi_transaction_done_mixin/) | Menambahkan proses workflow state done pada objek transaksi
[ssi_transaction_open_mixin](ssi_transaction_open_mixin/) | Menambahkan proses workflow state open pada objek transaksi
[ssi_transaction_pricelist_mixin](ssi_transaction_pricelist_mixin/) | Menambahkan pricelist pada objek transaksi
[ssi_transaction_ready_mixin](ssi_transaction_ready_mixin/) | Menambahkan proses workflow state ready pada objek transaksi
[ssi_transaction_salesperson_mixin](ssi_transaction_salesperson_mixin/) | Menambahkan salesperson pada objek transaksi
[ssi_transaction_win_lost_mixin](ssi_transaction_win_lost_mixin/) | Menambahkan proses workflow win/lost pada objek transaksi
[ssi_transaction_cancel_mixin](ssi_transaction_cancel_mixin/) | Menambahkan proses workflow state cancel pada objek transaksi
[ssi_transaction_terminate_mixin](ssi_transaction_terminate_mixin/) | Menambahkan proses workflow state terminate pada objek transaksi

Test Addons
-----------
addon | summary
--- | ---
[test_ssi_custom_information_mixin](test_ssi_custom_information_mixin/) | Modul test untuk custom information
[test_ssi_duration_mixin](test_ssi_duration_mixin/) | Modul test untuk duration
[test_ssi_multiple_approval_mixin](test_ssi_multiple_approval_mixin/) | Modul test untuk multiple approval
[test_ssi_policy_mixin](test_ssi_policy_mixin/) | Modul test untuk workflow policy
[test_ssi_product_line_account_mixin](test_ssi_product_line_account_mixin/) | Modul test untuk product line account
[test_ssi_product_line_mixin](test_ssi_product_line_mixin/) | Modul test untuk product line
[test_ssi_product_line_price_mixin](test_ssi_product_line_price_mixin/) | Modul test untuk product line price
[test_ssi_related_attachment_mixin](test_ssi_related_attachment_mixin/) | Modul test untuk related attachment
[test_ssi_sequence_mixin](test_ssi_sequence_mixin/) | Modul test untuk sequence policy
[test_ssi_state_change_constrain_mixin](test_ssi_state_change_constrain_mixin/) | Modul test untuk state change constrains
[test_ssi_status_check_mixin](test_ssi_status_check_mixin/) | Modul test untuk status check
[test_ssi_transaction_mixin](test_ssi_transaction_mixin/) | Modul test untuk objek transaction dan master data

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to OCA
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----

OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.
