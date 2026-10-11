.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: AGPL-3

======================
Accounting Entry Mixin
======================

``ssi_accounting_entry_mixin`` provides a set of abstract Odoo models that
standardise the creation, posting, and deletion of accounting entries
(``account.move`` and ``account.move.line``) from transactional documents.

The module ships four composable mixins:

* **mixin.account_move** — high-level helper for the journal-entry *header*:
  creates, posts, and cancels an ``account.move`` record with configurable
  field-name pointers and optional tax computation support.
* **mixin.account_move_single_line** — creates one ``account.move.line``
  inside an existing move; the normal direction (debit vs. credit) and all
  source fields are driven by class-level attributes.
* **mixin.account_move_double_line** — creates a balanced debit/credit pair
  of move lines in one call; each side is independently configurable.
* **mixin.tax_line** — ready-to-use child-record model for tax lines that
  references the appropriate tax account.

Concrete ``_with_field`` variants of each mixin add the actual Odoo storage
fields (``move_id``, ``move_line_id``, ``realized``, etc.) for cases where the
inheriting model needs to persist the generated entry references.


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Accounting Entry Mixin*
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
