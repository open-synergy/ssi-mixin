# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MixinCurrency(models.AbstractModel):
    """
    Abstract mixin for multi-currency transactional documents.

    Provides ``currency_id``, ``company_id``, ``rate_inverted``, and ``rate``
    fields together with helper methods to:

    * Automatically populate the exchange rate from the currency master when
      the currency or company changes (``onchange_rate_mixin``).
    * Convert amounts from the transaction currency to the company currency
      (``_convert_amount_to_company_currency``).

    Subclasses set ``_exchange_date_field`` to the name of the date field that
    should be used when looking up the historical exchange rate.
    """

    _name = "mixin.currency"
    _description = "Currency Mixin"
    _exchange_date_field = "date_transaction"

    @api.model
    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id

    currency_id = fields.Many2one(
        string="Transaction Currency",
        comodel_name="res.currency",
        required=True,
        default=lambda self: self._default_currency_id(),
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    rate_inverted = fields.Boolean(
        string="Rate Inverted",
    )
    rate = fields.Monetary(
        string="Transaction Rate",
        required=True,
        default=1.0,
    )

    @api.onchange(
        "currency_id",
    )
    def onchange_rate_inverted(self):
        self.rate_inverted = False
        if self.currency_id:
            self.rate_inverted = self.currency_id.rate_inverted

    @api.onchange(
        "currency_id",
        "company_id",
    )
    def onchange_rate_mixin(self):
        self.rate = 1.0
        date_exchange = getattr(self, self._exchange_date_field)
        if self.currency_id and self.company_id and date_exchange:
            rates = self.currency_id._get_rates(
                company=self.company_id,
                date=date_exchange,
            )
            self.rate = rates.get(self.company_id.id)

    def _convert_amount_to_company_currency(self, amount):
        if self.rate_inverted:
            result = amount * self.rate
        else:
            result = amount / self.rate
        return result
