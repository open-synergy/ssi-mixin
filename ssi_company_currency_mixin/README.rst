.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: AGPL-3

======================
Company Currency Mixin
======================

``ssi_company_currency_mixin`` provides a lightweight abstract Odoo model —
``mixin.company_currency`` — that adds a company field and its derived
currency to any model.

Any model that inherits from ``mixin.company_currency`` automatically gains:

* A mandatory ``company_id`` (``res.company``) field defaulting to the
  current user’s company.
* A stored, related ``company_currency_id`` field that always reflects the
  selected company’s currency.

Monetary fields on child models can set ``currency_field='company_currency_id'``
to format amounts in the company’s currency without extra boilerplate.


Installation
============

To install this module, you need to:

1.  Clone the branch 19.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Company Currency Mixin*
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
