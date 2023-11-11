# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class MixinResUsersM2OConfigurator(models.AbstractModel):
    _name = "mixin.res_users_m2o_configurator"
    _inherit = [
        "mixin.decorator",
    ]
    _description = "res.users Many2one Configurator Mixin"

    _res_users_m2o_configurator_insert_form_element_ok = False
    _res_users_m2o_configurator_form_xpath = False

    user_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="User Selection Method",
        required=True,
    )
    user_ids = fields.Many2many(
        comodel_name="res.users",
        string="Users",
    )
    user_domain = fields.Text(default="[]", string="User Domain")
    user_python_code = fields.Text(default="result = []", string="User Python Code")

    @ssi_decorator.insert_on_form_view()
    def _res_users_m2o_configurator_insert_form_element(self, view_arch):
        # TODO
        template_xml = "ssi_res_users_m2o_configurator_mixin."
        template_xml += "res_users_m2o_configurator_template"
        if self._res_users_m2o_configurator_insert_form_element_ok:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id=template_xml,
                xpath=self._res_users_m2o_configurator_form_xpath,
                position="inside",
            )
        return view_arch
