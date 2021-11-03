# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError
from odoo.tools.safe_eval import safe_eval as eval


class MixinPolicy(models.AbstractModel):
    _name = "mixin.policy"
    _description = "Mixin Object for Workflow Policy"

    policy_template_id = fields.Many2one(
        string="# Template",
        comodel_name="policy.template",
    )

    @api.multi
    def _get_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    @api.multi
    def _evaluate_policy(self, template):
        self.ensure_one()
        if not template:
            return False
        try:
            method_name = "_evaluate_policy_" + template.computation_method
            result = getattr(self, method_name)(template)
        except Exception as error:
            msg_err = _("Error evaluating conditions.\n %s") % error
            raise UserError(msg_err)
        return result

    @api.multi
    def _evaluate_policy_use_python(self, template):
        self.ensure_one()
        res = False
        localdict = self._get_localdict()
        try:
            eval(template.python_code, localdict, mode="exec", nocopy=True)
            res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        return res

    @api.multi
    def _evaluate_policy_use_domain(self, template):
        self.ensure_one()
        result = False
        domain = [("id", "=", self.id)] + eval(template.domain, {})

        count_result = self.search_count(domain)
        if count_result > 0:
            result = True
        return result

    @api.multi
    def _get_template_id(self):
        result = False
        obj_policy_template = self.env["policy.template"]
        criteria = [
            ("model_id.model", "=", str(self._name)),
        ]
        policy_template_id = obj_policy_template.search(
            criteria,
            order="sequence desc",
            limit=1,
        )
        if self._evaluate_policy(policy_template_id):
            result = policy_template_id.id
        return result

    @api.depends(
        "policy_template_id",
    )
    @api.multi
    def _compute_policy(self):
        for document in self:
            if document.policy_template_id:
                for policy in document.policy_template_id.detail_ids:
                    result = policy.get_policy(document)
                    setattr(
                        document,
                        policy.field_id.name,
                        result,
                    )
