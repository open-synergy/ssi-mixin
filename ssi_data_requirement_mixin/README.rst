.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================
Data Requirement Mixin
======================

``ssi_data_requirement_mixin`` provides a complete framework for managing
document/data submission requirements between an organisation and its
partners.

The module ships the following components:

* **data_requirement_type_category** / **data_requirement_type** —
  master-data hierarchy that classifies required documents (e.g. KTP, NPWP,
  SIUP).
* **data_requirement_package_type** / **data_requirement_package** —
  groups a set of required types into a package (e.g. “Onboarding Docs”)
  and tracks the fulfilment workflow (draft → confirm → done / cancel).
* **data_requirement** — a single requirement raised against a partner,
  supporting submission via URL, file attachment, or free text.
* **mixin.data_requirement** — adds requirement tracking to any document
  model via a ``data_requirement_ids`` One2many.
* **mixin.data_requirement_configurator** — configures which packages are
  applicable for a given document type.


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Data Requirement Mixin*
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
* Miftahussalam <miftahussalam08@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
