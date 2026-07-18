.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: AGPL-3

=============
QR Code Mixin
=============
``ssi_qr_code_mixin`` provides an abstract Odoo model — ``mixin.qr_code``
— that adds a computed QR-code image to any model.

Any model that inherits from ``mixin.qr_code`` automatically gains:

* ``qr_image`` (Binary) — a computed QR-code image in PNG format encoded as
  Base64.
* Content strategy per model configured via the extended ``ir.model``:
  either use the standard web URL of the record, or supply custom Python
  code that builds the string to encode.
* Optional automatic injection of a QR-code page into the form view
  (enabled by setting ``_qr_code_create_page = True`` on the subclass).

The module depends on the ``qrcode`` Python library (listed in
``requirements.txt``) and on ``ssi_decorator`` for view injection.

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *QR Code Mixin*
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
