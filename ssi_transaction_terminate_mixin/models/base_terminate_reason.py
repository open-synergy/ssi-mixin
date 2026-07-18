# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BaseTerminateReason(models.Model):
    """
    Master-data model that stores the available reasons for terminating a
    transaction. Linked to models via ``ir.model.terminate_reason_ids`` and
    used as a required field by ``mixin.transaction_terminate``.
    """

    _name = "base.terminate_reason"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Terminate Reason"
    _field_name_string = "Terminate Reason"

    global_use = fields.Boolean(
        string="Global Use",
        default=False,
    )
