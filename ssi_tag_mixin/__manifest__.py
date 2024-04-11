# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Tag Mixin",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_master_data_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        # "templates/mixin_tag_templates.xml",
        "menu.xml",
        "views/global_tag_category_views.xml",
        "views/global_tag_views.xml",
        "views/ir_model_views.xml",
    ],
    "demo": [
        # "demo/global_tag_demo.xml",
    ],
}
