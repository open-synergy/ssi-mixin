# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Data Requirement Mixin + Operating Unit",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_data_requirement_mixin",
        "ssi_operating_unit_mixin",
    ],
    "data": [
        "security/res_group/data_requirement.xml",
        "security/res_group/data_requirement_package.xml",
        "security/ir_rule/data_requirement.xml",
        "security/ir_rule/data_requirement_package.xml",
        "view/data_requirement.xml",
        "view/data_requirement_package.xml",
    ],
}
