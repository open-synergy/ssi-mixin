.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: AGPL-3

==================
Print Policy Mixin
==================

``ssi_print_mixin`` provides a standardised print-document framework that adds
a configurable *Print* button to any Odoo model via an abstract mixin.

The module ships the following components:

* **mixin.print_document** — abstract mixin that automatically injects a
  *Print* button into the form-view header and list-view header when
  ``_automatically_insert_print_button = True`` on the subclass.
* **print_document_type** — a named document type (scoped to a specific
  model) that groups the reports available for printing; its ``code`` is
  generated from a sequence.
* **ir.actions.report** extension — adds ``print_document_type_ids`` to link
  reports to types, a ``print_python_code`` condition evaluated at print time,
  and a ``print_multi`` flag for batch printing.


Installation
============

To install this module, you need to:

1.  Clone the branch 19.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Print Policy Mixin*
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
* Michael Viriyananda <viriyananda.michael@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
