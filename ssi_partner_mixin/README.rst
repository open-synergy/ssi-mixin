.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: AGPL-3

=============
Partner Mixin
=============
``ssi_partner_mixin`` provides an abstract Odoo model — ``mixin.partner``
— that adds configurable partner and contact fields to any document model.

Any model that inherits from ``mixin.partner`` automatically gains:

* ``partner_id`` (``res.partner``) — top-level company/individual partner.
* ``contact_partner_id`` (``res.partner``) — contact person under the
  selected partner, filtered via a computed ``allowed_contact_ids``.
* Computed boolean attributes (``mixin_partner_partner_id_required``,
  ``mixin_partner_partner_id_readonly``, etc.) that expose the effective
  required/readonly state of both partner fields, driven by class-level
  configuration and the record’s current state.
* Optional view injection into form, tree, and search views controlled by
  class-level ``_mixin_partner_insert_*`` and ``_xpath_*`` attributes.

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Partner Mixin*
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
