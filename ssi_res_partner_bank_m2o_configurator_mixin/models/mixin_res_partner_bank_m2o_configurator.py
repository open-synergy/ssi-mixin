# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class MixinResPartnerBankM2OConfigurator(models.AbstractModel):
    _name = "mixin.res_partner_bank_m2o_configurator"
    _inherit = [
        "mixin.decorator",
    ]
    _description = "res.partner.bank Many2one Configurator Mixin"

    _res_partner_bank_m2o_configurator_insert_form_element_ok = False
    _res_partner_bank_m2o_configurator_form_xpath = False

    partner_bank_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Partner Bank Selection Method",
        required=True,
    )
    partner_bank_ids = fields.Many2many(
        comodel_name="res.partner.bank",
        string="Partner Banks",
    )
    partner_bank_domain = fields.Text(default="[]", string="Partner Bank Domain")
    partner_bank_python_code = fields.Text(
        default="result = []", string="Partner Bank Python Code"
    )

    @ssi_decorator.insert_on_form_view()
    def _res_partner_bank_m2o_configurator_insert_form_element(self, view_arch):
        # TODO
        template_xml = "ssi_res_partner_bank_m2o_configurator_mixin."
        template_xml += "res_partner_bank_m2o_configurator_template"
        if self._res_partner_bank_m2o_configurator_insert_form_element_ok:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id=template_xml,
                xpath=self._res_partner_bank_m2o_configurator_form_xpath,
                position="inside",
            )
        return view_arch
