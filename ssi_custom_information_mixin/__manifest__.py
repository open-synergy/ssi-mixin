# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Custom Information Mixin",
    "version": "19.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "category": "Tools",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_decorator",
        "ssi_master_data_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "templates/custom_information_templates.xml",
        "views/custom_info_category_views.xml",
        "views/custom_info_template_views.xml",
        "views/custom_info_option_views.xml",
        "views/custom_info_option_set_views.xml",
        "views/custom_info_value_views.xml",
        "views/custom_info_property_views.xml",
    ],
    "demo": [
        "demo/custom_info_category.xml",
        "demo/custom_info_option.xml",
        "demo/custom_info_option_set.xml",
        "demo/custom_info_property.xml",
    ],
}
