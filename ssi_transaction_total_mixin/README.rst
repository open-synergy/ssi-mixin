.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================
Transaction Mixin - Total
=========================

``ssi_transaction_total_mixin`` extends ``mixin.transaction`` with computed
monetary totals.

Four complementary abstract mixins are provided:

* **mixin.transaction_untaxed** — ``amount_untaxed`` aggregated from product
  line details.
* **mixin.transaction_tax** — ``amount_tax`` aggregated from tax-detail lines.
* **mixin.transaction_total** — ``amount_total`` (untaxed + tax).
* **mixin.transaction_residual** — ``amount_residual`` and
  ``amount_realized`` derived from linked ``account.move.line`` records.

Each mixin has a ``*WithField`` variant that persists the amounts to database
columns.


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Transaction Mixin - Total*
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
