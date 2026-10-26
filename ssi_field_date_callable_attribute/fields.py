# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields


class DateCallable(fields.Date):
    """
    A subclass of ``fields.Date`` that evaluates callable values for the
    ``readonly``, ``required``, ``string``, and ``states`` attributes when
    the field attributes are computed (``_get_attrs``).

    This allows these attributes to be specified as ``@api.model`` methods
    (decorated with ``_get_date_*`` naming conventions) so that subclasses
    can customise them through class-level attribute overrides without
    redeclaring the field.

    .. note::
       Since Odoo 17 the ORM no longer supports the ``states`` field
       attribute. It is still accepted and resolved here so that callers
       keep working, but it has no effect on the field behaviour.

    After registration the class is also exposed as ``fields.DateCallable``
    for convenient import by other modules.
    """

    states = None
    _callable_attrs = ("readonly", "required", "string", "states")

    def _get_attrs(self, model_class, name):
        """Resolve callable attributes against the model class.

        :param model_class: model class the field is being set up on
        :param name: name of the field
        :return: the field parameter attributes, with every callable
            among ``readonly``, ``required``, ``string`` and ``states``
            replaced by the value it returns
        :rtype: dict
        """
        attrs = super()._get_attrs(model_class, name)
        for key in self._callable_attrs:
            value = attrs.get(key)
            if callable(value):
                attrs[key] = value(model_class)
        return attrs


fields.DateCallable = DateCallable
