# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BaseLostReason(models.Model):
    """
    Master-data model that stores the available reasons for marking a
    transaction as lost. Linked to models via ``ir.model.lost_reason_ids`` and
    used as a required field by ``mixin.transaction_win_lost``.
    """

    _name = "base.lost_reason"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Lost Reason"
    _field_name_string = "Lost Reason"

    global_use = fields.Boolean(
        string="Global Use",
        default=False,
    )
