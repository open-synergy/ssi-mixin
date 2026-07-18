.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: AGPL-3

=============
Backend Mixin
=============
``ssi_backend_mixin`` provides an abstract Odoo model — ``backend_mixin`` —
that serves as a reusable base for *backend configuration* records scoped to a
company (e.g. accounting settings, payroll parameters).

Any model that inherits from ``backend_mixin`` automatically gains:

* All standard fields from ``mixin.master_data`` (``name``, ``code``,
  ``active``, ``note``, chatter, print-document support).
* A mandatory ``company_id`` field.
* A ``state`` selection (``draft`` / ``running``) for activating the record.
* ``action_running`` — marks this record as *running* for the current company
  and deactivates any previously running record of the same type.
* ``action_restart`` — reverts the record to ``draft`` and clears the company
  reference pointer.

Subclasses configure ``_backend_company_field`` to the name of the
``res.company`` field that should store the currently active backend ID.

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Backend Mixin*
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

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
