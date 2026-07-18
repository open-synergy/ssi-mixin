# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class CustomInfoOption(models.Model):
    """
    A single selectable value for a custom information property of type
    ``Selection`` or ``Multiple Selection``.

    Options are grouped into ``custom_info.option_set`` records, which are
    then attached to ``custom_info.property`` records that require a
    controlled vocabulary.
    """

    _name = "custom_info.option"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Available options for a custom property"
    _order = "name"
