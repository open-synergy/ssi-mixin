.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================
Many2one Configurator Mixin
===========================
``ssi_m2o_configurator_mixin`` provides an abstract Odoo model —
``mixin.many2one_configurator`` — that implements a three-strategy runtime
filter for Many2one fields.

The three strategies are:

* **manual** — the allowed records are selected explicitly by the user.
* **domain** — a domain string (evaluated with ``safe_eval``) determines which
  records are allowed.
* **code** — arbitrary Python code is evaluated in a local dictionary
  (``env``, ``document``) and must assign a recordset to ``result``.

Concrete configurator models inherit this mixin and expose the strategy
fields to end users, enabling dynamic Many2one filtering without hard-coded
domains.

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Many2one Configurator Mixin*
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
