.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================
Terms and Conditions Mixin
==========================

``ssi_term_condition_mixin`` provides a full terms-and-conditions (T&C)
framework for transactional documents.

The module ships the following components:

* **tnc_template** — master-data T&C template with section and clause lines.
* **tnc_template.section** / **tnc_template.clause** — template-level
  section and clause records (inheriting ``mixin.tnc_section`` /
  ``mixin.tnc_clause``).
* **tnc_section** / **tnc_clause** — document-instance records that are
  created from the template when a document is confirmed.
* **mixin.tnc** — abstract mixin that links a document to a T&C template
  and instantiates section/clause records, with optional auto-injected
  form-view page.


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Terms and Conditions Mixin*
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
