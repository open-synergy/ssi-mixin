# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import api, fields, models


class MixinPartner(models.AbstractModel):
    """
    Abstract mixin that adds configurable ``partner_id`` and
    ``contact_partner_id`` fields together with view-injection hooks.

    Key features:

    * ``partner_id`` (``res.partner``) filtered to top-level partners.
    * ``contact_partner_id`` (``res.partner``) filtered to contacts of the
      selected partner via a computed ``allowed_contact_ids`` Many2many.
    * Computed boolean fields that expose the effective required/readonly
      attributes of both partner fields based on class-level configuration
      and the current record state — so views can use them in ``attrs``.
    * Optional view injection into form, tree, and search views controlled
      by class-level ``_mixin_partner_insert_*`` flags and ``_xpath_*``
      attributes.
    """

    _name = "mixin.partner"
    _description = "Mixin for Object With Partner"

    _mixin_partner_insert_form = False
    _mixin_partner_xpath_form = "//field[@name='user_id']"
    _mixin_partner_xpath_page = "//page[last()]"

    _mixin_partner_insert_tree = False
    _mixin_partner_xpath_tree = "//field[@name='display_name']"

    _mixin_partner_insert_search = False
    _mixin_partner_xpath_search = "//field[@name='user_id']"
    _mixin_partner_xpath_group = "//filter[@name='grp_responsible']"

    _mixin_partner_partner_id_required = True
    _mixin_partner_partner_id_readonly = False
    _mixin_partner_contact_id_required = False
    _mixin_partner_contact_id_readonly = False

    _mixin_partner_partner_id_required_include_state = False
    _mixin_partner_partner_id_required_exclude_state = False
    _mixin_partner_partner_id_readonly_include_state = False
    _mixin_partner_partner_id_readonly_exclude_state = ["draft"]
    _mixin_partner_contact_id_required_include_state = False
    _mixin_partner_contact_id_required_exclude_state = False
    _mixin_partner_contact_id_readonly_include_state = False
    _mixin_partner_contact_id_readonly_exclude_state = ["draft"]

    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        domain=[
            ("parent_id", "=", False),
        ],
    )

    @api.depends(
        "partner_id",
    )
    def _compute_allowed_contact_ids(self):
        Partner = self.env["res.partner"]
        for record in self:
            result = []
            if record.partner_id:
                criteria = [
                    ("commercial_partner_id", "=", record.partner_id.id),
                    ("id", "!=", record.partner_id.id),
                    ("type", "=", "contact"),
                ]
                result = Partner.search(criteria).ids
            record.allowed_contact_ids = result

    allowed_contact_ids = fields.Many2many(
        string="Allowed Contact",
        comodel_name="res.partner",
        compute="_compute_allowed_contact_ids",
        store=False,
    )
    contact_partner_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
    )
    mixin_partner_partner_id_required = fields.Boolean(
        string="Mixin Partner - partner_id Required",
        compute="_compute_mixin_partner_attribute",
        store=False,
        compute_sudo=True,
    )
    mixin_partner_partner_id_readonly = fields.Boolean(
        string="Mixin Partner - parnter_id Readonly",
        compute="_compute_mixin_partner_attribute",
        store=False,
        compute_sudo=True,
    )
    mixin_partner_contact_id_required = fields.Boolean(
        string="Mixin Partner - contact_id Required",
        compute="_compute_mixin_partner_attribute",
        store=False,
        compute_sudo=True,
    )
    mixin_partner_contact_id_readonly = fields.Boolean(
        string="Mixin Partner - contact_id Readonly",
        compute="_compute_mixin_partner_attribute",
        store=False,
        compute_sudo=True,
    )

    @api.depends(
        "name",
    )
    def _compute_mixin_partner_attribute(self):
        for record in self:
            mixin_partner_partner_id_required = (
                mixin_partner_partner_id_readonly
            ) = (
                mixin_partner_contact_id_required
            ) = mixin_partner_contact_id_readonly = False

            if self._mixin_partner_partner_id_required:
                mixin_partner_partner_id_required = True
            elif (
                self._mixin_partner_partner_id_required_include_state
                and hasattr(self, "state")
                and record.state
                in self._mixin_partner_partner_id_required_include_state
            ):
                mixin_partner_partner_id_required = True
            elif (
                self._mixin_partner_partner_id_required_exclude_state
                and hasattr(self, "state")
                and record.state
                not in self._mixin_partner_partner_id_required_exclude_state
            ):
                mixin_partner_partner_id_required = True

            if self._mixin_partner_partner_id_readonly:
                mixin_partner_partner_id_readonly = True
            elif (
                self._mixin_partner_partner_id_readonly_include_state
                and hasattr(self, "state")
                and record.state
                in self._mixin_partner_partner_id_readonly_include_state
            ):
                mixin_partner_partner_id_readonly = True
            elif (
                self._mixin_partner_partner_id_readonly_exclude_state
                and hasattr(self, "state")
                and record.state
                not in self._mixin_partner_partner_id_readonly_exclude_state
            ):
                mixin_partner_partner_id_readonly = True

            if self._mixin_partner_contact_id_required:
                mixin_partner_contact_id_required = True
            elif (
                self._mixin_partner_contact_id_required_include_state
                and hasattr(self, "state")
                and record.state
                in self._mixin_partner_contact_id_required_include_state
            ):
                mixin_partner_contact_id_required = True
            elif (
                self._mixin_partner_contact_id_required_exclude_state
                and hasattr(self, "state")
                and record.state
                not in self._mixin_partner_contact_id_required_exclude_state
            ):
                mixin_partner_contact_id_required = True

            if self._mixin_partner_contact_id_readonly:
                mixin_partner_contact_id_readonly = True
            elif (
                self._mixin_partner_contact_id_readonly_include_state
                and hasattr(self, "state")
                and record.state
                in self._mixin_partner_contact_id_readonly_include_state
            ):
                mixin_partner_contact_id_readonly = True
            elif (
                self._mixin_partner_contact_id_readonly_exclude_state
                and hasattr(self, "state")
                and record.state
                not in self._mixin_partner_contact_id_readonly_exclude_state
            ):
                mixin_partner_contact_id_readonly = True

            record.mixin_partner_partner_id_required = mixin_partner_partner_id_required
            record.mixin_partner_partner_id_readonly = mixin_partner_partner_id_readonly
            record.mixin_partner_contact_id_required = mixin_partner_contact_id_required
            record.mixin_partner_contact_id_readonly = mixin_partner_contact_id_readonly

    @api.onchange(
        "partner_id",
    )
    def onchange_contact_partner_id(self):
        self.contact_partner_id = False

    def _mixin_partner_insert_view_node(self, doc, xpath, template_xml_ids):
        """
        Render one or more QWeb templates and insert them right after the
        node located by ``xpath`` in ``doc``.

        Each XML ID in ``template_xml_ids`` is rendered and inserted via
        ``addnext()`` on the same anchor node (``node_xpath[0]``), matching
        the original behavior: since every insertion targets the anchor
        itself (not the previously inserted node), the resulting sibling
        order after the anchor is the reverse of ``template_xml_ids``.

        :param doc: root ``etree`` element of the view arch being modified.
        :param xpath: XPath expression used to locate the anchor node.
        :param template_xml_ids: list of QWeb template XML IDs to render
            and insert, in the same order as the original insertion calls.
        :return: ``True`` if the anchor node was found and templates were
            inserted, ``False`` otherwise.
        """
        node_xpath = doc.xpath(xpath)
        if not node_xpath:
            return False

        for xml_id in template_xml_ids:
            str_element = self.env["ir.qweb"]._render(xml_id)
            new_node = etree.fromstring(str_element)
            node_xpath[0].addnext(new_node)
        return True

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        res = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        doc = etree.XML(res["arch"])
        if (
            view_type == "form"
            and self._mixin_partner_insert_form
            and self._mixin_partner_xpath_form
        ):
            self._mixin_partner_insert_view_node(
                doc,
                self._mixin_partner_xpath_form,
                [
                    "ssi_partner_mixin.allowed_contact_ids",
                    "ssi_partner_mixin.contact_id",
                    "ssi_partner_mixin.partner_id",
                ],
            )
            self._mixin_partner_insert_view_node(
                doc,
                self._mixin_partner_xpath_page,
                ["ssi_partner_mixin.mixin_partner_setting"],
            )
        elif (
            view_type == "tree"
            and self._mixin_partner_insert_tree
            and self._mixin_partner_xpath_tree
        ):
            self._mixin_partner_insert_view_node(
                doc,
                self._mixin_partner_xpath_tree,
                [
                    "ssi_partner_mixin.tree_contact_id",
                    "ssi_partner_mixin.tree_partner_id",
                ],
            )
        elif (
            view_type == "search"
            and self._mixin_partner_insert_search
            and self._mixin_partner_xpath_search
        ):
            self._mixin_partner_insert_view_node(
                doc,
                self._mixin_partner_xpath_search,
                [
                    "ssi_partner_mixin.search_contact_id",
                    "ssi_partner_mixin.search_partner_id",
                ],
            )
            self._mixin_partner_insert_view_node(
                doc,
                self._mixin_partner_xpath_group,
                [
                    "ssi_partner_mixin.group_contact_id",
                    "ssi_partner_mixin.group_partner_id",
                ],
            )

        View = self.env["ir.ui.view"]

        if view_id and res.get("base_model", self._name) != self._name:
            View = View.with_context(base_model_name=res["base_model"])
        new_arch, new_fields = View.postprocess_and_fields(doc, self._name)
        res["arch"] = new_arch
        new_fields.update(res["fields"])
        res["fields"] = new_fields
        return res
