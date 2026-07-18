.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: AGPL-3

===============
SSI - Decorator
===============

``ssi_decorator`` provides a view-decoration framework for Odoo 14 that
allows model methods to declaratively inject XML fragments into form, tree,
and search views at runtime.

Any model that inherits from ``mixin.decorator`` can define methods marked
with the SSI decorator tags:

* ``_insert_on_form_view`` — called to modify the form-view XML.
* ``_insert_on_tree_view`` — called to modify the list-view XML.
* ``_insert_on_search_view`` — called to modify the search-view XML.

During ``fields_view_get`` the mixin discovers all such methods via
introspection and runs them in order, allowing modules to extend views from
other modules entirely in Python without writing XML ``inherit`` records.


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *SSI - Decorator*
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
