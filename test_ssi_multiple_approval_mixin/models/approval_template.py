# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ApprovalTemplate(models.Model):
    _inherit = "approval.template"

    @api.model
    def _get_multiple_approval_model_names(self):
        res = super(ApprovalTemplate, self)._get_multiple_approval_model_names()
        res.append("test.multiple_approval")
        return res
