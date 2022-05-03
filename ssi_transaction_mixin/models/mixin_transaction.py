# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MixinTransaction(models.AbstractModel):
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
    _automatically_insert_view_element = False
    _statusbar_visible_label = "draft"
    _policy_field_xpath = (
        "/form/sheet/notebook/page[@name='policy']"
        "/group[@name='policy_2']/field[@name='restart_ok']"
    )

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

    def action_restart(self):
        for record in self.sudo():
            record.write(record._prepare_restart_data())

    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": self._draft_state,
        }

    def name_get(self):
        result = []
        for record in self:
            if record.name == "/":
                name = "*" + str(record.id)
            else:
                name = record.name
            result.append((record.id, name))
        return result

    def unlink(self):
        strWarning1 = _("You can only delete data on draft state")
        strWarning2 = _("You can only delete data without document number")
        force_unlink = self.env.context.get("force_unlink", False)
        for record in self:
            if record.state != "draft" and not force_unlink:
                raise UserError(strWarning1)
            if record.name != "/" and not force_unlink:
                raise UserError(strWarning2)
        _super = super(MixinTransaction, self)
        _super.unlink()

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        result = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        View = self.env["ir.ui.view"]

        view_arch = etree.XML(result["arch"])

        view_arch = self._reorder_header_button(view_arch, view_type)
        view_arch = self._reorder_policy_field(view_arch, view_type)
        view_arch = self._reconfigure_statusbar_visible(view_arch, view_type)

        if view_id and result.get("base_model", self._name) != self._name:
            View = View.with_context(base_model_name=result["base_model"])
        new_arch, new_fields = View.postprocess_and_fields(view_arch, self._name)
        result["arch"] = new_arch
        new_fields.update(result["fields"])
        result["fields"] = new_fields

        return result

    @api.model
    def _add_view_element(
        self, view_arch, qweb_template_xml_id, xpath, position="after", order=False
    ):
        additional_element = self.env["ir.qweb"]._render(qweb_template_xml_id)
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
    def _reorder_header_button(self, view_arch, view_type):
        if view_type == "form" and self._automatically_insert_view_element:
            node_xpath = view_arch.xpath("/form/header")[0]
            to_sort = (e for e in node_xpath if e.tag == "button")
            no_sort = (e for e in node_xpath if e.tag == "field")
            node_xpath[:] = sorted(
                to_sort, key=lambda child: child.get("order", 100)
            ) + list(no_sort)
        return view_arch

    @api.model
    def _reorder_policy_field(self, view_arch, view_type):
        if view_type == "form" and self._automatically_insert_view_element:
            node_xpath = view_arch.xpath(
                "/form/sheet/notebook/page[@name='policy']/group[@name='policy_2']"
            )[0]
            to_sort = (e for e in node_xpath if e.tag == "field")
            node_xpath[:] = sorted(to_sort, key=lambda child: child.get("order", 100))
        return view_arch

    @api.model
    def _reconfigure_statusbar_visible(self, view_arch, view_type):
        if view_type == "form" and self._automatically_insert_view_element:
            node_xpath = view_arch.xpath("/form/header/field[@name='state']")[0]
            node_xpath.set("statusbar_visible", self._statusbar_visible_label)
        return view_arch
