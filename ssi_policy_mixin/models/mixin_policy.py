# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError
from odoo.tools.safe_eval import safe_eval


class MixinPolicy(models.AbstractModel):
    _name = "mixin.policy"
    _description = "Mixin Object for Workflow Policy"

    @api.multi
    def _compute_allowed_policy_template_ids(self):
        obj_template = self.env["policy.template"]
        for record in self:
            criteria = [
                ("model", "=", self._name),
            ]
            record.allowed_policy_template_ids = obj_template.search(criteria).ids

    allowed_policy_template_ids = fields.Many2many(
        string="Allowed Policy Templates",
        comodel_name="policy.template",
        compute="_compute_allowed_policy_template_ids",
        store=False,
    )
    policy_template_id = fields.Many2one(
        string="Policy Template",
        comodel_name="policy.template",
        copy=False,
        domain=lambda self: [("model", "=", self._name)],
    )

    @api.multi
    def _get_policy_localdict(self):
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
        localdict = self._get_policy_localdict()
        try:
            safe_eval(template.python_code, localdict, mode="exec", nocopy=True)
            res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        return res

    @api.multi
    def _evaluate_policy_use_domain(self, template):
        self.ensure_one()
        result = False
        domain = [("id", "=", self.id)] + safe_eval(template.domain, {})

        count_result = self.search_count(domain)
        if count_result > 0:
            result = True
        return result

    @api.multi
    def _get_template_policy(self):
        result = False
        obj_policy_template = self.env["policy.template"]
        criteria = [
            ("model_id.model", "=", str(self._name)),
        ]
        policy_templates = obj_policy_template.search(
            criteria,
            order="sequence desc",
        )
        for template in policy_templates:
            if self._evaluate_policy(template):
                result = template.id
                break
        return result

    @api.multi
    def action_reload_policy_template(self):
        for record in self:
            record.write(
                {
                    "policy_template_id": self._get_template_policy(),
                }
            )

    @api.depends(
        "policy_template_id",
    )
    @api.multi
    def _compute_policy(self):
        for document in self:
            if document.policy_template_id:
                for policy in document.policy_template_id.detail_ids:
                    result = policy.get_policy(document)
                    if policy.field_id:
                        setattr(
                            document,
                            policy.field_id.name,
                            result,
                        )
