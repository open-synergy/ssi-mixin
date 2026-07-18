# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BaseCancelReason(models.Model):
    """
    Master-data model that stores the available reasons for cancelling a
    transaction. Linked to models via ``ir.model.cancel_reason_ids`` and used
    as a required field by ``mixin.transaction_cancel``.
    """

    _name = "base.cancel_reason"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Cancel Reason"
    _field_name_string = "Cancel Reason"

    global_use = fields.Boolean(
        string="Global Use",
        default=False,
    )
