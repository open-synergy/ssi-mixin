# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import fields

_logger = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class DateCallable(fields.Date):
    # pylint: disable=access-member-before-definition,attribute-defined-outside-init
    def _setup_attrs(self, model, name):
        result = super()._setup_attrs(model, name)
        readonly_attr = self.readonly
        if readonly_attr and callable(readonly_attr):
            self.readonly = readonly_attr(model)

        required_attr = self.required
        if required_attr and callable(required_attr):
            self.required = required_attr(model)

        string_attr = self.string
        if string_attr and callable(string_attr):
            self.string = string_attr(model)

        states_attr = self.states
        if states_attr and callable(states_attr):
            self.states = states_attr(model)
        return result


fields.DateCallable = DateCallable
