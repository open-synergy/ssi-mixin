# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=W0622
from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError
from odoo.tools.safe_eval import safe_eval


class StatusCheck(models.Model):
    _name = "status.check"
    _description = "Status Check"

    model = fields.Char(
        string="Related Document Model",
        index=True,
    )
    res_id = fields.Integer(
        string="Related Document ID",
        index=True,
    )
    template_id = fields.Many2one(
        string="# Template",
        comodel_name="status.check.template",
    )
    template_detail_id = fields.Many2one(
        string="# Template Detail",
        comodel_name="status.check.template_detail",
    )
    status_check_method = fields.Selection(
        related="template_detail_id.status_check_item_id.status_check_method",
        readonly=True,
    )
    status_check_item_id = fields.Many2one(
        related="template_detail_id.status_check_item_id",
        readonly=True,
    )

    @api.multi
    def _compute_status_ok(self):
        for document in self:
            document.status_ok = False
            result = document._evaluate_status_check()
            if result:
                document.status_ok = result

    status_ok = fields.Boolean(
        string="Status Ok",
        compute="_compute_status_ok",
    )

    @api.multi
    def _get_document(self):
        document_id = self.res_id
        document_model = self.model

        object = self.env[document_model].browse([document_id])[0]
        return object

    @api.multi
    def _get_localdict(self):
        return {
            "document": self._get_document(),
            "env": self.env,
        }

    @api.multi
    def _evaluate_status_check(self):
        self.ensure_one()
        if not self.template_detail_id:
            return False
        try:
            method_name = "_evaluate_status_check_" + self.status_check_method
            result = getattr(self, method_name)()
        except Exception as error:
            msg_err = _("Error evaluating conditions.\n %s") % error
            raise UserError(msg_err)
        return result

    @api.multi
    def _evaluate_status_check_use_python(self):
        self.ensure_one()
        res = False
        localdict = self._get_localdict()
        try:
            safe_eval(
                self.status_check_item_id.python_code,
                localdict,
                mode="exec",
                nocopy=True,
            )
            if "result" in localdict:
                res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        return res
