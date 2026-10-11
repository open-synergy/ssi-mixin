.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
Duration Mixin
==============
``ssi_duration_mixin`` provides two abstract Odoo models for recording time
spans on any document.

* **mixin.date_duration** — adds ``date_start`` and ``date_end`` date fields
  using ``DateCallable`` for fully configurable labels, required/readonly
  states, and a built-in constraint that enforces ``date_end >= date_start``.
  All field attributes (required, readonly, string, state overrides) are
  driven by class-level attributes, so subclasses need no field re-declarations.

* **mixin.datetime_duration** — a simpler variant that adds plain
  ``Datetime`` start and end fields for cases where date-level precision is
  sufficient and extended configurability is not needed.

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Duration Mixin*
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
