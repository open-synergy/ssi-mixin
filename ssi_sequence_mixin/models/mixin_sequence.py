# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import _, api, models
from odoo.exceptions import Warning as UserError
from odoo.tools.safe_eval import safe_eval


class MixingSequence(models.AbstractModel):
    _name = "mixin.sequence"
    _description = "Mixin Object for Sequence Policy"

    _fallback_sequence_field = "name"

    @api.multi
    def _get_sequence_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    @api.multi
    def _evaluate_sequence(self, template):
        self.ensure_one()
        if not template:
            return False
        try:
            method_name = "_evaluate_sequence_" + template.computation_method
            result = getattr(self, method_name)(template)
        except Exception as error:
            msg_err = _("Error evaluating conditions.\n %s") % error
            raise UserError(msg_err)
        return result

    @api.multi
    def _evaluate_sequence_use_python(self, template):
        self.ensure_one()
        res = False
        localdict = self._get_sequence_localdict()
        try:
            safe_eval(template.python_code, localdict, mode="exec", nocopy=True)
            res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        return res

    @api.multi
    def _evaluate_sequence_use_domain(self, template):
        self.ensure_one()
        result = False
        domain = [("id", "=", self.id)] + safe_eval(template.domain, {})

        count_result = self.search_count(domain)
        if count_result > 0:
            result = True
        return result

    @api.multi
    def _get_template_sequence(self):
        result = False
        obj_sequence_template = self.env["sequence.template"]
        criteria = [
            ("model_id.model", "=", str(self._name)),
        ]
        templates = obj_sequence_template.search(
            criteria,
            order="sequence desc",
        )
        for template in templates:
            if self._evaluate_sequence(template):
                result = template
                break
        return result

    @api.multi
    def _create_sequence(self):
        self.ensure_one()
        template = self._get_template_sequence()
        if template:
            result = template.initial_string
            if getattr(self, template.sequence_field_id.name) == result:
                result = template.create_sequence(self)
            else:
                result = getattr(self, template.sequence_field_id.name)
        else:
            result = getattr(self, self._fallback_sequence_field)

        return result
