# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields

_logger = logging.getLogger(__name__)


class DateCallable(fields.Date):
    """
    A subclass of ``fields.Date`` that evaluates callable values for the
    ``readonly``, ``required``, ``string``, and ``states`` attributes at
    field-setup time (``_setup_attrs``).

    This allows these attributes to be specified as ``@api.model`` methods
    (decorated with ``_get_date_*`` naming conventions) so that subclasses
    can customise them through class-level attribute overrides without
    redeclaring the field.

    After registration the class is also exposed as ``fields.DateCallable``
    for convenient import by other modules.
    """

    def _setup_attrs(self, model, name):
        super()._setup_attrs(model, name)
        readonly_attr = self.readonly
        if self.readonly and callable(readonly_attr):
            self.readonly = readonly_attr(model)

        required_attr = self.required
        if self.required and callable(readonly_attr):
            self.required = required_attr(model)

        string_attr = self.string
        if self.string and callable(string_attr):
            self.string = string_attr(model)

        states_attr = self.states
        if self.states and callable(states_attr):
            self.states = states_attr(model)


fields.DateCallable = DateCallable
