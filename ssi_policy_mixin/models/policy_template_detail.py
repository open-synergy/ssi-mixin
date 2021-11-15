# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import Warning as UserError
from odoo.tools.safe_eval import safe_eval


class PolicyTemplateDetail(models.Model):
    _name = "policy.template_detail"
    _description = "Policy Template Detail"

    template_id = fields.Many2one(
        string="# Template",
        comodel_name="policy.template",
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        related="template_id.company_id",
        store=True,
    )
    field_id = fields.Many2one(
        string="Field",
        comodel_name="ir.model.fields",
        domain="[('model_id', '=', parent.model_id)]",
    )
    active = fields.Boolean(
        default=True,
    )
    restrict_state = fields.Boolean(
        string="Restriction Based on State",
        default=True,
    )
    states = fields.Char(
        string="States",
    )
    restrict_user = fields.Boolean(
        string="Restriction Based on User",
        default=True,
    )
    computation_method = fields.Selection(
        string="User Evaluation Method",
        selection=[
            ("use_user", "Specific User"),
            ("use_group", "Any User In Specific Groups"),
            ("use_both", "Both Specific User And Group"),
            ("use_python", "Python Expression"),
        ],
        default="use_user",
        required=True,
    )
    user_ids = fields.Many2many(
        string="Users",
        comodel_name="res.users",
        relation="rel_policy_template_detail_2_user",
        column1="detail_id",
        column2="user_id",
    )
    group_ids = fields.Many2many(
        string="Groups",
        comodel_name="res.groups",
        relation="rel_policy_template_detail_2_group",
        column1="detail_id",
        column2="group_id",
    )
    python_code = fields.Text(
        string="Python Code",
        default="""# Available locals:\n#  - rec: current record\n result = []""",
    )
    restrict_additional = fields.Boolean(
        string="Restriction Based on Additional Python Code",
        default=False,
    )
    additional_python_code = fields.Text(
        string="Additional Python Code",
        default="""# Available locals:\n#  - rec: current record\n result = True""",
    )

    @api.multi
    def _get_localdict(self, document):
        self.ensure_one()
        return {
            "env": self.env,
            "document": document,
        }

    @api.multi
    def _get_policy(self, document):
        self.ensure_one()
        result_state = True
        result_user = True
        result_additional = True

        if self.restrict_state:
            if not self._evaluate_states(document):
                result_state = False

        if self.restrict_user:
            if self.env.user.id == SUPERUSER_ID:
                result_user = True
            else:
                try:
                    method_name = "_get_policy_" + self.computation_method
                    result_user = getattr(self, method_name)(document)
                except Exception as error:
                    msg_err = _("Error evaluating conditions.\n %s") % error
                    raise UserError(msg_err)

        if self.restrict_additional:
            localdict = self._get_localdict(document)
            try:
                safe_eval(
                    self.additional_python_code, localdict, mode="exec", nocopy=True
                )
                result_additional = localdict["result"]
            except Exception as error:
                msg_err = _("Error evaluating conditions.\n %s") % error
                raise UserError(msg_err)

        return result_state and result_user and result_additional

    @api.multi
    def _get_policy_use_user(self, document):
        self.ensure_one()
        result = False
        current_user = self.env.user
        user_ids = self.user_ids
        if set(user_ids) & set(current_user):
            result = True
        return result

    @api.multi
    def _get_policy_use_group(self, document):
        self.ensure_one()
        result = False
        current_user = self.env.user
        current_group_ids = current_user.groups_id.ids
        group_ids = self.group_ids.ids
        if set(group_ids) & set(current_group_ids):
            result = True
        return result

    @api.multi
    def _get_policy_use_both(self, document):
        self.ensure_one()
        result = False
        current_user = self.env.user
        current_group_ids = current_user.groups_id.ids
        group_ids = self.group_ids.ids
        user_ids = self.user_ids
        if (set(group_ids) & set(current_group_ids)) or (
            set(user_ids) & set(current_user)
        ):
            result = True
        return result

    @api.multi
    def _get_policy_use_python(self, document):
        self.ensure_one()
        result = False
        localdict = self._get_localdict(document)
        try:
            safe_eval(self.python_code, localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        return result

    @api.multi
    def _evaluate_states(self, document):
        self.ensure_one()
        result = False
        if self.template_id.state_field_id:
            state_field = getattr(document, self.template_id.state_field_id.name)
            list_states = self.states.split(",")
            if state_field in list_states:
                result = True
        return result

    @api.multi
    def get_policy(self, document):
        self.ensure_one()
        policy = self._get_policy(document)
        return policy
