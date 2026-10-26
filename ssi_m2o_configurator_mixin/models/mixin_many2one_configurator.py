# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class MixinMany2oneConfigurator(models.AbstractModel):
    """
    Abstract mixin that implements a three-strategy filter for Many2one
    field domains: ``manual`` (explicit recordset), ``domain`` (ORM domain
    string evaluated with ``safe_eval``), or ``code`` (arbitrary Python code
    evaluated in a local dictionary).

    Concrete configurator models inherit this and expose the strategy fields
    (``method_selection``, ``manual_ids``, ``domain``, ``python_code``) so
    that users can pick the most appropriate filtering method at runtime.
    """

    _name = "mixin.many2one_configurator"
    _description = "Many2one Configurator Mixin"

    def _m2o_configurator_get_filter(
        self, object_name, method_selection, manual_recordset, domain, python_code
    ):
        """Return the records allowed by the configured filter strategy.

        :param str object_name: Technical name of the model to filter.
        :param str method_selection: One of ``manual``, ``domain``
            or ``code``.
        :param manual_recordset: Records returned for ``manual``.
        :param str domain: Domain string used for ``domain``.
        :param str python_code: Python code used for ``code``.
        :return: Filtered recordset.
        """
        self.ensure_one()

        if method_selection == "manual":
            result = manual_recordset
        elif method_selection == "domain":
            result = self._m2o_configurator_get_filter_by_domain(object_name, domain)
        elif method_selection == "code":
            result = self._m2o_configurator_get_filter_by_code(python_code)

        return result

    def _m2o_configurator_get_filter_by_domain(self, object_name, domain):
        """Search ``object_name`` using a domain string.

        :param str object_name: Technical name of the model to search.
        :param str domain: Domain evaluated with ``safe_eval``.
        :return: Matching recordset.
        """
        self.ensure_one()
        domain = safe_eval(domain, {})
        return self.env[object_name].search(domain)

    def _m2o_configurator_get_filter_by_code(self, python_code):
        """Evaluate Python code that assigns ``result``.

        :param str python_code: Code evaluated with ``safe_eval``.
        :return: Value assigned to ``result`` by the code.
        :raises UserError: If the evaluation fails.
        """
        self.ensure_one()
        localdict = self._m2o_configurator_get_localdict()
        try:
            safe_eval(
                python_code,
                localdict,
                mode="exec",
            )
            result = localdict["result"]
        except Exception as error:
            raise UserError(
                self.env._("Error evaluating conditions.\n %s", error)
            ) from error
        return result

    def _m2o_configurator_get_localdict(self):
        """Build the local dictionary used by the code strategy.

        :return: Dictionary exposing ``env`` and ``document``.
        :rtype: dict
        """
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }
