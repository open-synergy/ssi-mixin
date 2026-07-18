# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import html

from odoo import api, models


class MixinPrintDocument(models.AbstractModel):
    """
    Abstract mixin that enables a standardised *Print* button on any document
    model.

    When ``_automatically_insert_print_button`` is set to ``True`` on a
    subclass, the mixin injects the print button into the form header (at the
    XPath configured by ``_print_button_xpath``) and into the list-view header
    automatically during ``_get_view``.

    The actual rendering and report selection is delegated to
    ``print_document_type`` records linked via ``ir.actions.report``.
    """

    _name = "mixin.print_document"
    _description = "Print Document Mixin"

    # Attributes related to automatically insert elemnt on form view
    _automatically_insert_print_button = False
    _print_button_xpath = "/form/header/field[@name='state']"
    _print_button_position = "before"

    @api.model
    def _get_view(self, view_id=None, view_type="form", **options):
        view_arch, view = super()._get_view(
            view_id=view_id, view_type=view_type, **options
        )

        if view_type == "form":
            view_arch = self._view_add_form_print_button(view_arch)
        elif view_type == "list":
            view_arch = self._view_add_tree_print_button(view_arch)

        return view_arch, view

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

    @api.model
    def _view_add_tree_print_button(self, view_arch):
        if self._automatically_insert_print_button:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_print_mixin.tree_button_print",
                "/list/header",
                "inside",
            )
        return view_arch

    @api.model
    def _view_add_form_print_button(self, view_arch):
        if self._automatically_insert_print_button:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_print_mixin.button_ssi_print",
                self._print_button_xpath,
                self._print_button_position,
            )
        return view_arch
