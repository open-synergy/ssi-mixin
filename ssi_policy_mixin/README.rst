.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: AGPL-3

============
Policy Mixin
============

``ssi_policy_mixin`` provides an abstract Odoo model — ``mixin.policy`` — that
implements a *policy-template* mechanism for controlling which action buttons
are available on a document at any given time.

Each inheriting model declares boolean policy fields (e.g. ``confirm_ok``,
``cancel_ok``) via ``_get_policy_field`` and links to a ``policy.template``
that evaluates Python conditions against the current record to set those fields
automatically.

* **policy.template** — master-data record holding Python evaluation code
  (matching criteria) and ordered detail lines.
* **policy.template.detail** — maps a policy field to its computed value
  for records that match the template.
* ``action_reload_policy_template`` — manually re-selects the active
  template based on the record’s current state.


Installation
============

To install this module, you need to:

1.  Clone the branch 19.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Policy Mixin*
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

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
