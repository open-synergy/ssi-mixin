.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================
Source Document Mixin
=====================

``ssi_source_document_mixin`` provides an abstract Odoo model —
``mixin.source_document`` — that adds a lightweight polymorphic source-
document reference to any model.

Rather than using Odoo’s schema-heavy ``fields.Reference`` column, the mixin
stores the reference as two fields:

* ``source_document_model_id`` (``ir.model``) — the model of the source.
* ``source_document_res_id`` (Integer) — the ID of the source record.

A computed ``source_document_id`` (``fields.Reference``) assembles those two
values into a navigable reference displayed in the UI, avoiding extra schema
migrations while still supporting cross-model linking.


Installation
============

To install this module, you need to:

1.  Clone the branch 41.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps*
5.  Search For *Source Document Mixin*
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
   :target: https://simetri-sinergi.id.com

This module is maintained by the PT. Simetri Sinergi Indonesia.
