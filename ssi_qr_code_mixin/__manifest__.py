# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "QR Code Mixin",
    "version": "14.0.2.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_decorator",
    ],
    "external_dependencies": {
        "python": [
            "qrcode",
        ],
    },
    "data": [
        "templates/mixin_qr_code_templates.xml",
        "views/ir_model_views.xml",
    ],
}
