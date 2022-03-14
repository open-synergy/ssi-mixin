# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class MixinRelatedAttachment(models.AbstractModel):
    _name = "mixin.related_attachment"
    _description = "Mixin Object for Related Attachment"

    def _compute_allowed_related_attachment_template_ids(self):
        obj_template = self.env["attachment.related_attachment_template"]
        for record in self:
            criteria = [("model", "=", self._name)]
            result = obj_template.search(criteria).ids
            record.allowed_related_attachment_template_ids = result

    related_attachment_template_id = fields.Many2one(
        string="Related Attachment Template",
        comodel_name="attachment.related_attachment_template",
        copy=False,
        domain=lambda self: [("model", "=", self._name)],
    )
    allowed_related_attachment_template_ids = fields.Many2many(
        string="Allowed Related Attachment Template",
        comodel_name="attachment.related_attachment_template",
        compute="_compute_allowed_related_attachment_template_ids",
        store=False,
    )
    related_attachment_ids = fields.One2many(
        string="Related Attachments",
        comodel_name="attachment.related_attachment",
        inverse_name="res_id",
        domain=lambda self: [("model", "=", self._name)],
        auto_join=True,
    )

    def _get_related_attachment_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def _evaluate_related_attachment(self, template):
        self.ensure_one()
        if not template:
            return False
        try:
            method_name = "_evaluate_related_attachment_" + template.computation_method
            result = getattr(self, method_name)(template)
        except Exception as error:
            msg_err = _("Error evaluating conditions.\n %s") % error
            raise UserError(msg_err)
        return result

    def _evaluate_related_attachment_use_python(self, template):
        self.ensure_one()
        res = False
        localdict = self._get_related_attachment_localdict()
        try:
            safe_eval(template.python_code, localdict, mode="exec", nocopy=True)
            if "result" in localdict:
                res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        return res

    def _evaluate_related_attachment_domain(self, template):
        self.ensure_one()
        result = False
        domain = [("id", "=", self.id)] + safe_eval(template.domain, {})

        count_result = self.search_count(domain)
        if count_result > 0:
            result = True
        return result

    def _get_template_related_attachment(self):
        result = False
        obj_related_attachment_template = self.env[
            "attachment.related_attachment_template"
        ]
        criteria = [
            ("model_id.model", "=", str(self._name)),
        ]
        template_id = obj_related_attachment_template.search(
            criteria,
            limit=1,
        )
        if self._evaluate_related_attachment(template_id):
            result = template_id.id
        return result

    @api.onchange()
    def _onchange_related_attachment_template_id(self):
        self.related_attachment_template_id = False
        template_id = self._get_template_related_attachment()
        self.related_attachment_template_id = template_id

    @api.onchange(
        "related_attachment_template_id",
    )
    def onchange_related_attachment_ids(self):
        res = []
        if self.related_attachment_ids:
            to_check = self.related_attachment_ids.mapped("attachment_id")
            if to_check:
                error_msg = _("Attachment already exist")
                raise UserError(_("%s") % (error_msg))
        self.related_attachment_ids = [(5, 0, 0)]
        if self.related_attachment_template_id:
            res = self.create_related_attachment_ids()
        self.related_attachment_ids = res

    def create_related_attachment_ids(self):
        self.ensure_one()
        obj_related_attachment_template_detail = self.env[
            "attachment.related_attachment_template_detail"
        ]
        obj_related_attachment = res = self.env["attachment.related_attachment"]
        sequence = 0

        criteria = [("template_id", "=", self.related_attachment_template_id.id)]
        related_attachment_ids = obj_related_attachment_template_detail.search(
            criteria, order="sequence"
        )
        if related_attachment_ids:
            for related_attachment in related_attachment_ids:
                sequence += 1
                res += obj_related_attachment.create(
                    {
                        "model": self._name,
                        "res_id": self.id,
                        "template_id": self.related_attachment_template_id.id,
                        "template_detail_id": related_attachment.id,
                    }
                )
        return res

    def unlink(self):
        related_attachments = self.mapped("related_attachment_ids")
        res = super(MixinRelatedAttachment, self).unlink()
        if res:
            related_attachments.unlink()
        return res
