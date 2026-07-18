# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class GlobalTagCategory(models.Model):
    """
    Master-data model (inheriting ``mixin.master_data``) that groups
    ``global_tag`` records into named categories.

    The ``exclusive`` flag indicates that only one tag from this category may
    be applied to a document at a time. Setting ``global_use`` makes the
    category automatically available for all models without explicit
    model-level assignment.
    """

    _name = "global_tag_category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Global Tag Category"
    _order = "id, sequence"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
    )
    color = fields.Integer(
        string="Color Index",
    )
    exclusive = fields.Boolean(
        string="Exclusive",
    )
    global_use = fields.Boolean(
        string="Global Use",
        default=False,
    )
