# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MixinTransaction(models.AbstractModel):
    """
    Abstract model to transaction object
    """

    _name = "mixin.transaction"
    _inherit = [
        "mail.activity.mixin",
        "mail.thread",
        "mixin.sequence",
        "mixin.policy",
    ]
    _description = "Transaction Mixin"
    _draft_state = "draft"
    _create_sequence_state = False
    _document_number_field = "name"
    _automatically_insert_view_element = False

    _automatically_reconfigure_statusbar_visible = True
    _policy_field_order = False
    _header_button_order = False

    _statusbar_visible_label = "draft"
    _policy_field_xpath = (
        "/form/sheet/notebook/page[@name='policy']"
        "/group[@name='policy_2']/field[@name='restart_ok']"
    )

    # Attributes related to add element on search view automatically
    _state_filter_xpath = "/search/group[@name='dom_state']/filter[@name='dom_draft']"
    _state_filter_order = False

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
        copy=True,
    )

    @api.model
    def _default_user_id(self):
        return self.env.user.id

    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        required=True,
        default=lambda self: self._default_user_id(),
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    note = fields.Text(
        string="Note",
        copy=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
        ],
        default="draft",
        required=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.multi
    def _compute_policy(self):
        _super = super(MixinTransaction, self)
        _super._compute_policy()

    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )
    manual_number_ok = fields.Boolean(
        string="Can Input Manual Document Number",
        compute="_compute_policy",
    )

    @api.multi
    def action_restart(self):
        for record in self.sudo():
            record.write(record._prepare_restart_data())

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": self._draft_state,
        }

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if getattr(record, self._document_number_field) == "/":
                name = "*" + str(record.id)
            else:
                name = record.name
            result.append((record.id, name))
        return result

    @api.multi
    def unlink(self):
        force_unlink = self.env.context.get("force_unlink", False)
        for record in self:
            if not record._check_state_unlink(force_unlink):
                error_message = """
                Context: Delete {}
                Database ID: {}
                Problem: Document state is not draft
                Solution: Cancel and restart document
                """.format(
                    self._description.lower(),
                    record.id,
                )
                raise UserError(_(error_message))
            if not record._check_document_number_unlink(force_unlink):
                error_message = """
                Context: Delete {}
                Database ID: {}
                Problem: Document number is not equal to /
                Solution: Change document number into /
                """.format(
                    self._description.lower(),
                    record.id,
                )
                raise UserError(_(error_message))
        _super = super(MixinTransaction, self)
        _super.unlink()

    # TODO: Dynamic field name
    @api.constrains(
        "name",
    )
    def _constrains_duplicate_document_number(self):
        for record in self.sudo():
            if not record._check_duplicate_document_number():
                error_message = """
                Context: Change {} document number
                Database ID: {}
                Problem: Duplicate document number
                Solution: Change document number into different number
                """.format(
                    self._description.lower(),
                    record.id,
                )
                raise UserError(_(error_message))

    @api.multi
    def _check_document_number_unlink(self, force_unlink=False):
        self.ensure_one()
        result = True
        if getattr(self, self._document_number_field) != "/" and not force_unlink:
            result = False
        return result

    @api.multi
    def _check_state_unlink(self, force_unlink=False):
        self.ensure_one()
        result = True
        if self.state != "draft" and not force_unlink:
            result = False
        return result

    @api.multi
    def _check_duplicate_document_number(self):
        self.ensure_one()
        result = True
        criteria = [
            (
                self._document_number_field,
                "=",
                getattr(self, self._document_number_field),
            ),
            (self._document_number_field, "!=", "/"),
            ("id", "!=", self.id),
        ]
        ObjectMixin = self.env[self._name]
        count_duplicate = ObjectMixin.search_count(criteria)
        if count_duplicate > 0:
            result = False
        return result

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        res = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        view_model = self.env["ir.ui.view"]
        view_arch = etree.XML(res["arch"])
        if view_type == "form" and self._automatically_insert_view_element:
            view_arch = self._reorder_header_button(view_arch)
            view_arch = self._reorder_policy_field(view_arch)
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        elif view_type == "search" and self._automatically_insert_view_element:
            view_arch = self._reorder_state_filter_on_search_view(view_arch)

        if view_id and res.get("base_model", self._name) != self._name:
            view_model = view_model.with_context(base_model_name=res["base_model"])
        new_arch, new_fields = view_model.postprocess_and_fields(
            self._name, view_arch, res["view_id"]
        )
        res["arch"] = new_arch
        new_fields.update(res["fields"])
        res["fields"] = new_fields
        return res

    @api.model
    def _add_view_element(
        self, view_arch, qweb_template_xml_id, xpath, position="after", order=False
    ):
        additional_element = self.env["ir.qweb"].render(qweb_template_xml_id)
        if len(view_arch.xpath(xpath)) == 0:
            return view_arch
        node_xpath = view_arch.xpath(xpath)[0]
        new_node = etree.fromstring(additional_element)
        if order:
            new_node.set("order", str(order))
        if position == "after":
            node_xpath.addnext(new_node)
        elif position == "before":
            node_xpath.addprevious(new_node)
        return view_arch

    @api.model
    def _reorder_header_button(self, view_arch):
        if not self._header_button_order:
            return view_arch
        _xpath = "/form/header"
        if len(view_arch.xpath(_xpath)) == 0:
            return view_arch
        node_xpath = view_arch.xpath(_xpath)[0]
        for node in node_xpath:
            if node.get("name") in self._header_button_order:
                node.set(
                    "order", str(self._header_button_order.index(node.get("name")))
                )
        to_sort = (e for e in node_xpath if e.tag == "button")
        no_sort = (e for e in node_xpath if e.tag == "field")
        node_xpath[:] = sorted(
            to_sort, key=lambda child: int(child.get("order", "100"))
        ) + list(no_sort)
        return view_arch

    @api.model
    def _reorder_policy_field(self, view_arch):
        if not self._policy_field_order:
            return view_arch
        _xpath = "/form/sheet/notebook/page[@name='policy']/group[@name='policy_2']"
        if len(view_arch.xpath(_xpath)) == 0:
            return view_arch
        node_xpath = view_arch.xpath(_xpath)[0]
        for node in node_xpath:
            if node.get("name") in self._policy_field_order:
                node.set("order", str(self._policy_field_order.index(node.get("name"))))
        to_sort = (e for e in node_xpath if e.tag == "field")
        node_xpath[:] = sorted(
            to_sort, key=lambda child: int(child.get("order", "100"))
        )
        return view_arch

    @api.model
    def _reconfigure_statusbar_visible(self, view_arch):
        if not self._automatically_reconfigure_statusbar_visible:
            return view_arch
        _xpath = "/form/header/field[@name='state']"
        if len(view_arch.xpath(_xpath)) == 0:
            return view_arch
        node_xpath = view_arch.xpath(_xpath)[0]
        node_xpath.set("statusbar_visible", self._statusbar_visible_label)
        return view_arch

    @api.model
    def _reorder_state_filter_on_search_view(self, view_arch):
        if not self._state_filter_order:
            return view_arch
        _xpath = "/search/group[@name='dom_state']"  # TODO: Make it as class attribute
        if len(view_arch.xpath(_xpath)) == 0:
            return view_arch
        node_xpath = view_arch.xpath(_xpath)[0]
        for node in node_xpath:
            if node.get("name") in self._state_filter_order:
                node.set("order", str(self._state_filter_order.index(node.get("name"))))
        to_sort = (e for e in node_xpath if e.tag == "filter")
        node_xpath[:] = sorted(
            to_sort, key=lambda child: int(child.get("order", "100"))
        )
        return view_arch
