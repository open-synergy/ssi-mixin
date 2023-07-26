# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class MixinMany2oneConfigurator(models.AbstractModel):
    _name = "mixin.many2one_configurator"
    _description = "Many2one Configurator Mixin"

    def _m2o_configurator_get_filter(
        self, object_name, method_selection, manual_recordset, domain, python_code
    ):
        self.ensure_one()

        if method_selection == "manual":
            result = manual_recordset
        elif method_selection == "domain":
            result = self._m2o_configurator_get_filter_by_domain(object_name, domain)
        elif method_selection == "code":
            result = self._m2o_configurator_get_filter_by_code(python_code)

        return result

    def _m2o_configurator_get_filter_by_domain(self, object_name, domain):
        self.ensure_one()
        domain = safe_eval(domain, {})
        return self.env[object_name].search(domain)

    def _m2o_configurator_get_filter_by_code(self, python_code):
        self.ensure_one()
        localdict = self._m2o_configurator_get_localdict()
        try:
            safe_eval(
                python_code,
                localdict,
                mode="exec",
                nocopy=True,
            )
            result = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        return result

    def _m2o_configurator_get_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }
