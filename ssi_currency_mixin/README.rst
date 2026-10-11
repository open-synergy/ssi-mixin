.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
Currency Mixin
==============
``ssi_currency_mixin`` provides an abstract Odoo model — ``mixin.currency``
— that standardises multi-currency handling on transactional documents.

Any model that inherits from ``mixin.currency`` automatically gains:

* ``currency_id`` — the transaction currency, defaulting to the company’s
  currency.
* ``company_id`` — the owning company.
* ``rate_inverted`` — mirrors the ``rate_inverted`` flag from the currency
  master.
* ``rate`` — the exchange rate in use for the transaction date.
* ``onchange_rate_mixin`` — auto-fills ``rate`` from the currency master
  whenever ``currency_id`` or ``company_id`` changes.
* ``_convert_amount_to_company_currency`` — helper that converts a
  transaction-currency amount to the company currency using ``rate`` and
  ``rate_inverted``.

Subclasses set ``_exchange_date_field`` to the name of the date field used
for historical rate look-ups.

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Currency Mixin*
6.  Install the module

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/ssi-mixin/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Andhitia Rama <andhitia.r@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
