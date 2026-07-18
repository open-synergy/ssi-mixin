# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class MixinPolicy(models.AbstractModel):
    """
    Abstract mixin that implements the *policy-template* workflow control
    mechanism.

    Each inheriting model declares a list of boolean policy fields (via
    ``_get_policy_field``) such as ``confirm_ok``, ``cancel_ok``, etc. The
    mixin evaluates the matching ``policy.template`` against the current record
    (using safe-eval Python code) and writes the result booleans back to those
    fields, effectively controlling which action buttons are visible/enabled.

    The active template is auto-selected on record creation via
    ``_get_template_policy`` and can be reloaded manually through
    ``action_reload_policy_template``.
    """

    _name = "mixin.policy"
    _description = "Mixin Object for Workflow Policy"

    @api.model
    def _get_policy_field(self):
        res = []
        return res

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

    def _get_policy_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def _evaluate_policy(self, template):
        self.ensure_one()
        res = False
        localdict = self._get_policy_localdict()
        try:
            safe_eval(template.python_code, localdict, mode="exec")
            res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error) from error
        return res

    def _get_template_policy(self):
        self.ensure_one()
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

    def action_reload_policy_template(self):
        for record in self:
            record.write(
                {
                    "policy_template_id": record._get_template_policy(),
                }
            )

    def _prepare_policy_field_data(self):
        data = {}
        policy_field = self._get_policy_field()
        if policy_field:
            for policy in policy_field:
                data[policy] = False
        return data

    @api.depends(
        "policy_template_id",
    )
    def _compute_policy(self):
        for document in self:
            data = document._prepare_policy_field_data()
            if document.policy_template_id:
                for detail in document.policy_template_id.detail_ids:
                    result = detail.get_policy(document)
                    data[detail.field_id.name] = result
            for key in data:
                setattr(
                    document,
                    key,
                    data.get(key),
                )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for result in records:
            if not result.policy_template_id:
                template_id = result._get_template_policy()
                if template_id:
                    result.write({"policy_template_id": template_id})
        return records
