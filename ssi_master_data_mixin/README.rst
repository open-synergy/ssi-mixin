.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: AGPL-3

=================
Master Data Mixin
=================

Description
===========

``ssi_master_data_mixin`` provides an abstract Odoo model — ``mixin.master_data``
— that serves as a reusable base for **master/reference data** records.

Any model that inherits from ``mixin.master_data`` automatically gains:

* **Standard fields** — ``name`` (translatable), ``code`` (unique identifier),
  ``active`` (archive / restore), and ``note`` (free-text remarks).
* **Sequence generation** — a *Generate Code* button that assigns a
  sequence-based code from a configured sequence template.  Records whose
  ``code`` is ``'/'`` are treated as "unassigned" and can receive an automatic
  code at any time.
* **Unique-code constraint** — a SQL-level constraint prevents two records of
  the same model from sharing the same non-slash code.
* **Chatter integration** — inherits ``mail.thread`` and
  ``mail.activity.mixin``, giving the form view a full messaging thread and
  activity scheduler.
* **Print-document support** — inherits ``mixin.print_document`` and
  automatically injects a *Print* button into the form header.
* **Configurable display name** — by setting ``_show_code_on_display_name =
  True`` on a concrete model, the display name is rendered as ``[code] name``
  throughout the UI.

Typical use-cases: product types, work-order categories, payment terms,
school grades, or any static reference table that modules need to configure
once and reuse across transactions.

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Master Data Mixin*
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

* Michael Viriyananda <viriyananda.michael@gmail.com>
* Andhitia Rama <andhitia.r@gmail.com>
* Asrul Bastian Yunas <asrulbastianyunas@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
