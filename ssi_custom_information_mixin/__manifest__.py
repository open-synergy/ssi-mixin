# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Custom Information Mixin",
    "version": "11.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "views/custom_info_category_views.xml",
        "views/custom_info_template_views.xml",
        "views/custom_info_property_views.xml",
        "views/custom_info_option_views.xml",
        "views/custom_info_option_set_views.xml",
        "views/custom_info_value_views.xml",
    ],
}
