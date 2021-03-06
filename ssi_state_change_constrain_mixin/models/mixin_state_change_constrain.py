# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class MixinStateChangeConstrain(models.AbstractModel):
    _name = "mixin.state_change_constrain"
    _description = "Mixin Object for State Change Constrain"

    state_change_constrain_template_id = fields.Many2one(
        string="State Change Constrain Template",
        comodel_name="state.change.constrain.template",
        domain=lambda self: [("model", "=", self._name)],
        copy=False,
    )

    @api.multi
    def _get_state_change_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    @api.multi
    def _evaluate_state_change(self, template):
        self.ensure_one()
        if not template:
            return False
        try:
            method_name = "_evaluate_state_change_" + template.computation_method
            result = getattr(self, method_name)(template)
        except Exception as error:
            msg_err = _("Error evaluating conditions.\n %s") % error
            raise UserError(msg_err)
        return result

    @api.multi
    def _evaluate_state_change_use_python(self, template):
        self.ensure_one()
        res = False
        localdict = self._get_state_change_localdict()
        try:
            safe_eval(template.python_code, localdict, mode="exec", nocopy=True)
            if "result" in localdict:
                res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        return res

    @api.multi
    def _evaluate_state_change_domain(self, template):
        self.ensure_one()
        result = False
        domain = [("id", "=", self.id)] + safe_eval(template.domain, {})

        count_result = self.search_count(domain)
        if count_result > 0:
            result = True
        return result

    @api.multi
    def _get_template_state_change(self):
        self.ensure_one()
        result = False
        obj_state_change_template = self.env["state.change.constrain.template"]
        criteria = [
            ("status_check_template_id", "=", self.status_check_template_id.id),
        ]
        template_id = obj_state_change_template.search(
            criteria,
            order="sequence desc",
            limit=1,
        )
        if self._evaluate_state_change(template_id):
            result = template_id.id
        return result

    @api.onchange(
        "status_check_template_id",
    )
    def onchange_state_change_constrain_template_id(self):
        for document in self:
            document.state_change_constrain_template_id = False
            if document.status_check_template_id:
                template_id = document._get_template_state_change()
                document.state_change_constrain_template_id = template_id

    @api.constrains(
        "state",
    )
    def _check_state_constrain(self):
        for document in self:
            if document.state_change_constrain_template_id:
                detail_ids = document.state_change_constrain_template_id.detail_ids
                check_detail_ids = detail_ids.filtered(
                    lambda r: r.state == document.state
                )
                if check_detail_ids:
                    status_check_item_ids = check_detail_ids.status_check_item_ids
                    status_check_ids = document.status_check_ids
                    for detail in status_check_item_ids:
                        status_check = status_check_ids.filtered(
                            lambda r: r.status_check_item_id.id == detail.id
                        )
                        if not status_check.status_ok:
                            item = status_check.status_check_item_id.name
                            msg_error = _("Check Status item: %s") % (item)
                            raise UserError(msg_error)
