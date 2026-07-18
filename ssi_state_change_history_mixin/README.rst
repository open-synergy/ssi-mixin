.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================
State Change History Mixin
==========================

``ssi_state_change_history_mixin`` provides an automatic audit trail of
workflow state transitions for any transactional document.

* **state_change_history** — concrete log model storing one entry per
  state transition: document model, record ID, date, previous state, new
  state, and optional cancel/terminate reason.
* **mixin.state_change_history** — abstract mixin that adds
  ``state_change_history_ids`` and hooks into transition actions to create
  log entries automatically. An optional form-view page can be injected
  (``_automatically_insert_state_change_history_page = True``).


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps*
5.  Search For *State Change History Mixin*
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
   :target: https://simetri-sinergi.id.com

This module is maintained by the PT. Simetri Sinergi Indonesia.
