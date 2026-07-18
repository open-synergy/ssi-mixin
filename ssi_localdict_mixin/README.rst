.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============
Localdict Mixin
===============
``ssi_localdict_mixin`` provides an abstract Odoo model —
``mixin.localdict`` — that supplies a standard ``_get_default_localdict``
method.

The method assembles a ready-to-use safe-eval context dictionary containing:
``env``, ``document``, ``time``, ``datetime``, ``dateutil``, ``timezone``,
``float_compare``, ``b64encode``, and ``b64decode``.

Models that need to evaluate user-supplied Python code (e.g. domain filters,
computed-by-code fields, or formula configurations) inherit this mixin to
avoid duplicating the context-building boilerplate.

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Localdict Mixin*
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
