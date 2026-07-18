.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================
Multiple Approval Mixin
=======================

``ssi_multiple_approval_mixin`` provides a configurable multi-step approval
workflow for any transactional document.

* **approval.template** — master-data template that defines the approval
  sequence for a model with ordered detail lines.
* **approval.template.detail** — one approval step with an approver
  (user/role) and configurable conditions.
* **approval.approval** — concrete approval record created per step when a
  document enters the approval flow.
* **mixin.multiple_approval** — abstract mixin adding the approval page,
  ``action_approve``, ``action_reject``, and auto form-view injection via
  ``mixin.decorator``.


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Multiple Approval Mixin*
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

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
