.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: AGPL-3

=================
Salesperson Mixin
=================

``ssi_salesperson_mixin`` provides an abstract Odoo model —
``mixin.salesperson`` — that adds sales team and salesperson selection to
any model.

Any model that inherits from ``mixin.salesperson`` automatically gains:

* ``sale_team_id`` (``crm.team``) — the sales team.
* ``salesperson_id`` (``res.users``) — the responsible salesperson.
* ``allowed_salesperson_ids`` — a computed Many2many filtered to team members
  (or all internal users if no team is selected).
* ``onchange_salesperson_id`` — clears the salesperson when the team changes.


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Salesperson Mixin*
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
