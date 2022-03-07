# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class MixinStatusCheck(models.AbstractModel):
    _name = "mixin.status_check"
    _description = "Mixin Object for Status Check"

    status_check_template_id = fields.Many2one(
        string="# Status Check Template",
        comodel_name="status.check.template",
        domain=lambda self: [("model", "=", self._name)],
    )
    status_check_ids = fields.One2many(
        string="Status Check",
        comodel_name="status.check",
        inverse_name="res_id",
        domain=lambda self: [("model", "=", self._name)],
        auto_join=True,
    )

    def _get_status_check_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

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

    def _evaluate_status_check_use_python(self, template):
        self.ensure_one()
        res = False
        localdict = self._get_status_check_localdict()
        try:
            safe_eval(template.python_code, localdict, mode="exec", nocopy=True)
            if "result" in localdict:
                res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        return res

    def _evaluate_status_check_domain(self, template):
        self.ensure_one()
        result = False
        domain = [("id", "=", self.id)] + safe_eval(template.domain, {})

        count_result = self.search_count(domain)
        if count_result > 0:
            result = True
        return result

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
        for document in self:
            res = []
            document.status_check_ids = [(5, 0, 0)]
            if document.status_check_template_id:
                res = document.create_status_check_ids()
            document.status_check_ids = res

    def create_status_check_ids(self):
        self.ensure_one()
        obj_status_check_detail = self.env["status.check.template_detail"]
        obj_status_check = res = self.env["status.check"]
        sequence = 0

        criteria = [("template_id", "=", self.status_check_template_id.id)]
        status_check_ids = obj_status_check_detail.search(criteria, order="sequence")
        if status_check_ids:
            for status_check in status_check_ids:
                sequence += 1
                res += obj_status_check.create(
                    {
                        "model": self._name,
                        "res_id": self.id,
                        "template_id": self.status_check_template_id.id,
                        "template_detail_id": status_check.id,
                    }
                )
        return res
