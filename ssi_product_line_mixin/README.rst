.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: AGPL-3

==================
Product Line Mixin
==================
``ssi_product_line_mixin`` provides an abstract Odoo model —
``mixin.product_line`` — for product-line child records in transactional
documents.

Any model that inherits from ``mixin.product_line`` automatically gains:

* ``product_id`` (``product.product``) and ``name`` (description).
* ``uom_quantity``, ``uom_id`` (with ``allowed_uom_ids`` filtered by the
  product’s UoM category), and a computed ``quantity`` converted to the
  product’s base UoM.
* ``note`` — free-text line remark.
* Onchange handlers to auto-fill description and UoM from the product.

Usage
=====

``mixin.product_line_multiplier`` is an opt-in mixin for lines whose
quantity is the product of several independent factors (for example
persons x days x times). ``mixin.product_line`` itself is unchanged.

The mixin is installed in two concrete models in the user module:

.. code-block:: python

    class MyLineFactor(models.Model):
        _name = "my.line_factor"
        _description = "My Line Factor"
        _inherit = ["mixin.product_line_multiplier_factor"]

        line_id = fields.Many2one(
            comodel_name="my.line",
            required=True,
            ondelete="cascade",
        )


    class MyLine(models.Model):
        _name = "my.line"
        _description = "My Line"
        _inherit = [
            "mixin.product_line",
            "mixin.product_line_multiplier",
        ]

        multiplier_ids = fields.One2many(
            comodel_name="my.line_factor",
            inverse_name="line_id",
        )

When a line has at least one factor, ``uom_quantity`` is the product of all
factors. Without factors the current value is kept, so it can still be
filled manually. Each ``factor`` must be greater than zero, and the factor
``uom_id`` is only a label that is not used in the calculation.

``line_id`` and ``multiplier_ids`` are not defined by the mixins because
their comodel differs for every user model.

Do not install ``mixin.product_line_multiplier`` on a model that already
defines its own ``uom_quantity``; the two definitions would conflict.

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Product Line Mixin*
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
