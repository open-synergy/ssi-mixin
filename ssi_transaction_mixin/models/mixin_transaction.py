# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from inspect import getmembers

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
        "mixin.decorator",
        "mixin.sequence",
        "mixin.policy",
        "mixin.print_document",
    ]
    _description = "Transaction Mixin"
    _draft_state = "draft"
    _create_sequence_state = False
    _document_number_field = "name"
    _automatically_insert_view_element = False
    _automatically_insert_print_button = True
    _automatically_insert_restart_button = True

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
        help="""Transaction/document number

* Unique indentifer of transaction
* Leave '/' to automatically generate number
* Change '/' into any number/identifier to manually assign number.
  Manual number assignment can be done in 'Draft' state
  Only user with 'Can Manualy Assign Number' policy can manually assign number.
* Transaction with number other than '/' can not be deleted.""",
    )

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
        copy=True,
        help="""Company that own the document

* Automatically filled with user's company.
  Default company can be changed""",
    )
    company_partner_id = fields.Many2one(
        string="Company Partner",
        related="company_id.partner_id",
        store=False,
        help="""Partner (res.partner) linked to the document's company

* Automatically follows 'company_id.partner_id'.
* Used for reporting/printing documents that require the company-level
  partner instead of the responsible user's partner.""",
    )

    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        required=True,
        default=lambda self: self._default_user_id(),
        copy=False,
        readonly=True,
        help="""User that responsible for document

* Create user can be different with responsible user
* Automatically filled with user that initiate document creation.
  Default responsible can be changed.""",
    )
    reviewer_id = fields.Many2one(
        string="Reviewer",
        comodel_name="res.users",
        required=False,
        copy=False,
        readonly=True,
        help="""User that responsible to review document

* Unless it configured to approve reviewer does not equal to approver""",
    )

    note = fields.Text(
        string="Note",
        copy=True,
        help="Free-form note attached to the document, used for any additional "
        "remarks or information related to the transaction.",
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
        help="""Workflow status of the document

* 'draft' is the only base state provided by this mixin.
* Other states (e.g. confirmed, done, cancel) are added by derivative mixin
  modules (such as confirm/done/cancel mixins) via 'selection_add'.""",
    )

    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
        compute_sudo=True,
        help="""Restart policy

* If active user can see and execute 'Restart' button""",
    )
    manual_number_ok = fields.Boolean(
        string="Can Input Manual Document Number",
        compute="_compute_policy",
        compute_sudo=True,
        help="""Manual number assignment policy

* If active user can edit document number""",
    )
    display_name = fields.Char(
        string="Display Name", compute="_compute_display_name", store=True, index=True
    )

    @api.depends(lambda self: [self._document_number_field])
    def _compute_display_name(self):
        for record in self:
            if getattr(record, self._document_number_field) == "/":
                record.display_name = "*" + str(record.id)
            else:
                record.display_name = record.name

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_user_id(self):
        return self.env.user.id

    def _compute_policy(self):
        _super = super()
        _super._compute_policy()

    # TODO: Dynamic field name
    @api.constrains(
        "name",
    )
    def _constrains_duplicate_document_number(self):
        for record in self.sudo():
            if not record._check_duplicate_document_number():
                error_message = f"""
                Document Type: {self._description.lower()}
                Context: Change document number
                Database ID: {record.id}
                Problem: Duplicate document number
                Solution: Change document number into different number
                """
                raise UserError(_(error_message))

    def unlink(self):
        force_unlink = self.env.context.get("force_unlink", False)
        for record in self:
            if not record._check_state_unlink(force_unlink):
                error_message = f"""
                Document Type: {self._description.lower()}
                Context: Delete document
                Database ID: {record.id}
                Problem: Document state is not draft
                Solution: Cancel and restart document
                """
                raise UserError(_(error_message))
            if not record._check_document_number_unlink(force_unlink):
                error_message = f"""
                Document Type: {self._description.lower()}
                Context: Delete document
                Database ID: {record.id}
                Problem: Document number is not equal to /
                Solution: Change document number into /
                """
                raise UserError(_(error_message))
        _super = super()
        _super.unlink()

    @api.model
    def _get_view(self, view_id=None, view_type="form", **options):
        view_arch, view = super()._get_view(
            view_id=view_id, view_type=view_type, **options
        )

        if view_type == "form" and self._automatically_insert_view_element:
            view_arch = self._reorder_header_button(view_arch)
            view_arch = self._reorder_policy_field(view_arch)
        elif view_type == "search" and self._automatically_insert_view_element:
            view_arch = self._reorder_state_filter_on_search_view(view_arch)

        return view_arch, view

    def action_restart(self):
        for record in self.sudo():
            record._check_restart_policy()
            record._run_pre_restart_check()
            record._run_pre_restart_action()
            record.write(record._prepare_restart_data())
            record._run_post_restart_check()
            record._run_post_restart_action()
            record._notify_restart_action()

    def action_reset_document_number(self):
        for record in self.sudo():
            record._check_reset_number_policy()
            record._reset_document_number()

    def _reset_document_number(self):
        self.ensure_one()
        self.write(
            {
                "name": "/",
            }
        )

    def _check_reset_number_policy(self):
        self.ensure_one()

        if self.env.context.get("bypass_policy_check", False):
            return True

        if not self.manual_number_ok:
            error_message = f"""
            Document Type: {self._description}
            Context: Reset document number
            Database ID: {self.id}
            Problem: Reset document is no allowed
            Solution: Check restart policy prerequisite
            """
            raise UserError(_(error_message))

    def _notify_restart_action(self):
        self.ensure_one()
        msg = self._prepare_restart_action_notification()
        self.message_post(
            body=_(msg), message_type="notification", subtype_xmlid="mail.mt_note"
        )

    def _prepare_restart_action_notification(self):
        self.ensure_one()
        msg = f"{self._description} {self.display_name} restarted"
        return msg

    def _check_restart_policy(self):
        self.ensure_one()

        if not self._automatically_insert_restart_button:
            return True

        if self.env.context.get("bypass_policy_check", False):
            return True

        if not self.restart_ok:
            error_message = f"""
            Document Type: {self._description.lower()}
            Context: Restart document
            Database ID: {self.id}
            Problem: Document is not allowed to restart
            Solution: Check restart policy prerequisite
            """
            raise UserError(_(error_message))

    def _run_pre_restart_check(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_pre_restart_check"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_post_restart_check(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_post_restart_check"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_pre_restart_action(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_pre_restart_action"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_post_restart_action(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_post_restart_action"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": self._draft_state,
        }

    def _check_document_number_unlink(self, force_unlink=False):
        self.ensure_one()
        result = True
        if getattr(self, self._document_number_field) != "/" and not force_unlink:
            result = False
        return result

    def _check_state_unlink(self, force_unlink=False):
        self.ensure_one()
        result = True
        if self.state != "draft" and not force_unlink:
            result = False
        return result

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
