# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class MixinStatusCheck(models.AbstractModel):
    _name = "mixin.status_check"
    _description = "Mixin Object for Status Check"

    status_check_template_id = fields.Many2one(
        string="# Template",
        comodel_name="status.check.template",
    )
    status_check_ids = fields.One2many(
        string="Status Check",
        comodel_name="status.check",
        inverse_name="res_id",
        domain=lambda self: [("model", "=", self._name)],
        auto_join=True,
    )

    @api.multi
    def _get_policy_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    @api.multi
    def _evaluate_status_check(self, template):
        self.ensure_one()
        if not template:
            return False
        try:
            method_name = "_evaluate_status_check_" + template.computation_method
            result = getattr(self, method_name)(template)
        except Exception as error:
            msg_err = _("Error evaluating conditions.\n %s") % error
            raise UserError(msg_err)
        return result

    @api.multi
    def _evaluate_status_check_use_python(self, template):
        self.ensure_one()
        res = False
        localdict = self._get_policy_localdict()
        try:
            safe_eval(template.python_code, localdict, mode="exec", nocopy=True)
            if "result" in localdict:
                res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        return res

    @api.multi
    def _evaluate_status_check_domain(self, template):
        self.ensure_one()
        result = False
        domain = [("id", "=", self.id)] + safe_eval(template.domain, {})

        count_result = self.search_count(domain)
        if count_result > 0:
            result = True
        return result

    @api.multi
    def _get_template_status_check(self):
        result = False
        obj_status_check_template = self.env["status.check.template"]
        criteria = [
            ("model_id.model", "=", str(self._name)),
        ]
        template_id = obj_status_check_template.search(
            criteria,
            order="sequence desc",
            limit=1,
        )
        if self._evaluate_status_check(template_id):
            result = template_id.id
        return result

    @api.onchange(
        "status_check_template_id",
    )
    def onchange_status_check_ids(self):
        res = []
        self.status_check_ids = [(5, 0, 0)]
        if self.status_check_template_id:
            res = self.create_status_check_ids()
        self.status_check_ids = res

    @api.multi
    def create_status_check_ids(self):
        self.ensure_one()
        obj_approval_template_detail = self.env["status.check.template_detail"]
        obj_approval_approval = created_trs = self.env["status.check"]
        sequence = 0

        criteria_approval = [("template_id", "=", self.status_check_template_id.id)]
        approver_ids = obj_approval_template_detail.search(
            criteria_approval, order="sequence"
        )
        if approver_ids:
            for approver in approver_ids:
                sequence += 1
                created_trs += obj_approval_approval.create(
                    {
                        "model": self._name,
                        "res_id": self.id,
                        "template_id": self.status_check_template_id.id,
                        "template_detail_id": approver.id,
                        "sequence": sequence,
                    }
                )
        return created_trs
