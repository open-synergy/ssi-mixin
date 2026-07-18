# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from inspect import getmembers

from lxml import html

from odoo import api, models


class MixinDecorator(models.AbstractModel):
    """
    View-decoration framework that allows methods on an Odoo model to
    declaratively inject XML fragments into form, tree, and search views.

    Methods decorated with the SSI decorator markers (``_insert_on_form_view``,
    ``_insert_on_tree_view``, ``_insert_on_search_view``) are discovered via
    introspection during ``_get_view`` and called in sequence to modify
    the view architecture before it is returned to the client.

    Concrete models inherit this mixin (and ``mixin.master_data`` or
    ``mixin.transaction``) and then add decorator-marked methods to
    programmatically extend views from other modules without writing XML
    ``inherit`` records.
    """

    _name = "mixin.decorator"
    _description = "SSI Decorator Mixin"

    @api.model
    def _get_view(self, view_id=None, view_type="form", **options):
        view_arch, view = super()._get_view(
            view_id=view_id, view_type=view_type, **options
        )

        if view_type == "form":
            view_arch = self._run_insert_on_form_view(view_arch)
        elif view_type == "search":
            view_arch = self._run_insert_on_search_view(view_arch)
        elif view_type == "list":
            view_arch = self._run_insert_on_tree_view(view_arch)

        return view_arch, view

    @api.model
    def _run_insert_on_tree_view(self, view_arch):
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_api_model_decorator(func, "_insert_on_tree_view"):
                methods.append(func)
        if methods:
            view_arch = self.run_decorator_field_view_get_method(methods, view_arch)
        return view_arch

    @api.model
    def _run_insert_on_search_view(self, view_arch):
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_api_model_decorator(func, "_insert_on_search_view"):
                methods.append(func)
        if methods:
            view_arch = self.run_decorator_field_view_get_method(methods, view_arch)
        return view_arch

    @api.model
    def _run_insert_on_form_view(self, view_arch):
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_api_model_decorator(func, "_insert_on_form_view"):
                methods.append(func)
        if methods:
            view_arch = self.run_decorator_field_view_get_method(methods, view_arch)
        return view_arch

    def is_decorator(self, func, decorator):
        self.ensure_one()
        return callable(func) and hasattr(func, decorator)

    def run_decorator_method(self, methods):
        self.ensure_one()
        for method_name in methods:
            getattr(self, method_name.__name__)()

    def is_api_model_decorator(self, func, decorator):
        return callable(func) and hasattr(func, decorator)

    def run_decorator_field_view_get_method(self, methods, view_arch):
        for method_name in methods:
            view_arch = getattr(self, method_name.__name__)(view_arch)
        return view_arch

    @api.model
    def _add_view_element(
        self, view_arch, qweb_template_xml_id, xpath, position="after", order=False
    ):
        additional_element = self.env["ir.qweb"]._render(qweb_template_xml_id)
        if len(view_arch.xpath(xpath)) == 0:
            return view_arch
        node_xpath = view_arch.xpath(xpath)[0]
        for frag in html.fragments_fromstring(additional_element):
            if order:
                frag.set("order", str(order))
            if position == "after":
                node_xpath.addnext(frag)
            elif position == "before":
                node_xpath.addprevious(frag)
            elif position == "inside":
                node_xpath.insert(0, frag)
        return view_arch
