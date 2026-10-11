.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================================
Transaction Mixin - Queue To Done State
=======================================

``ssi_transaction_queue_done_mixin`` extends both ``mixin.transaction_done``
and ``mixin.transaction_queue`` to implement a *queued completion* workflow
state.

* Adds ``queue_to_done_ok`` policy field and auto-injects the queue-done
  button into the form view.
* Provides ``action_queue_done`` which creates a queue job that then
  executes the actual done action in the background.
* Configurable via ``_queue_to_done_state`` class attribute.


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Transaction Mixin - Queue To Done State*
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
