# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from inspect import getmembers

from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class MixinTransactionQueueCancel(models.AbstractModel):
    _name = "mixin.transaction_queue_cancel"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_queue",
    ]
    _description = "Transaction Mixin - Queue To Cancel State Mixin"
    _queue_to_cancel_state = "queue_cancel"

    # Attributes related to add element on form view automatically
    _automatically_insert_queue_cancel_policy_fields = True
    _automatically_insert_queue_cancel_button = True
    _queue_to_cancel_insert_form_element_ok = False
    _queue_to_cancel_form_xpath = False

    # Attributes related to add element on search view automatically
    _automatically_insert_queue_cancel_filter = True

    # Attributes related to add element on tree view automatically
    _automatically_insert_queue_cancel_state_badge_decorator = True

    # Attributes related to cancel reason wizard
    _method_to_run_from_wizard = "action_cancel"

    _auto_enqueue_cancel = True

    state = fields.Selection(
        selection_add=[
            ("queue_cancel", "Queue To Cancel"),
            ("cancel",),
        ],
        ondelete={
            "queue_cancel": "set default",
        },
    )
    queue_cancel_ok = fields.Boolean(
        string="Can Start Cancel Queue",
        compute="_compute_policy",
        compute_sudo=True,
    )
    cancel_queue_job_batch_id = fields.Many2one(
        string="To Cancel Queue Job Batch",
        comodel_name="queue.job.batch",
        readonly=True,
    )
    cancel_queue_job_ids = fields.One2many(
        string="To Cancel Queue Jobs",
        comodel_name="queue.job",
        related="cancel_queue_job_batch_id.job_ids",
        store=False,
    )
    cancel_queue_job_batch_state = fields.Selection(
        string="To Cancel Queue Job Batch State",
        related="cancel_queue_job_batch_id.state",
    )

    def _compute_policy(self):
        _super = super(MixinTransactionQueueCancel, self)
        _super._compute_policy()

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        result = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        View = self.env["ir.ui.view"]

        view_arch = etree.XML(result["arch"])
        if view_id and result.get("base_model", self._name) != self._name:
            View = View.with_context(base_model_name=result["base_model"])
        new_arch, new_fields = View.postprocess_and_fields(view_arch, self._name)
        result["arch"] = new_arch
        new_fields.update(result["fields"])
        result["fields"] = new_fields

        return result

    def action_requeue_cancel(self):
        for record in self.sudo():
            record._requeue_cancel_job_batch()

    def action_queue_cancel(self, cancel_reason=False):
        for record in self.sudo():
            record._check_queue_cancel_policy()
            record._run_pre_queue_cancel_check()
            record._create_job_batch_cancel()
            record._run_pre_queue_cancel_action()
            record.write(record._prepare_queue_cancel_data(cancel_reason))
            record._run_post_queue_cancel_check()
            record._run_post_queue_cancel_action()
            record._start_auto_enqueue_cancel()
            record._set_cancel_if_no_job()

    def _start_auto_enqueue_cancel(self):
        self.ensure_one()
        if self._auto_enqueue_cancel:
            self.cancel_queue_job_batch_id.enqueue()

    def action_recompute_queue_cancel_result(self):
        for record in self.sudo():
            record._recompute_queue_cancel_result()

    @ssi_decorator.post_cancel_action()
    def _disconnect_cancel_batch(self):
        self.ensure_one()

        if not self.cancel_queue_job_ids:
            self.cancel_queue_job_batch_id.write(
                {
                    "state": "finished",
                }
            )

        self.write(
            {
                "cancel_queue_job_batch_id": False,
            }
        )

    @ssi_decorator.insert_on_tree_view()
    def _to_insert_queue_cancel_button_to_tree_view(self, view_arch):
        template_xml = "ssi_transaction_queue_cancel_mixin."
        template_xml += "tree_button_queue_cancel"
        if self._automatically_insert_queue_cancel_button:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id=template_xml,
                xpath="/tree/header",
                position="inside",
            )
        return view_arch

    @ssi_decorator.insert_on_tree_view()
    def _to_insert_queue_cancel_state_badge_decorator(self, view_arch):
        if self._automatically_insert_queue_cancel_state_badge_decorator:
            _xpath = "/tree/field[@name='state']"
            if len(view_arch.xpath(_xpath)) == 0:
                return view_arch
            node_xpath = view_arch.xpath(_xpath)[0]
            node_xpath.set("decoration-success", "state == 'queue_cancel'")
        return view_arch

    @ssi_decorator.insert_on_search_view()
    def _to_insert_queue_cancel_filter_on_search_view(self, view_arch):
        template_xml = "ssi_transaction_queue_cancel_mixin."
        template_xml += "queue_cancel_filter"
        if self._automatically_insert_queue_cancel_filter:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id=template_xml,
                xpath=self._state_filter_xpath,
                position="after",
            )
        view_arch = self._reorder_state_filter_on_search_view(view_arch)
        return view_arch

    @ssi_decorator.insert_on_form_view()
    def _to_insert_queue_cancel_policy_field_to_form_view(self, view_arch):
        template_xml = "ssi_transaction_queue_cancel_mixin."
        template_xml += "queue_cancel_policy_field"
        if self._automatically_insert_queue_cancel_policy_fields:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id=template_xml,
                xpath=self._policy_field_xpath,
                position="before",
            )
        return view_arch

    @ssi_decorator.insert_on_form_view()
    def _to_insert_queue_cancel_button_to_form_view(self, view_arch):
        template_xml = "ssi_transaction_queue_cancel_mixin."
        template_xml += "button_queue_cancel"
        if self._automatically_insert_queue_cancel_button:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id=template_xml,
                xpath="/form/header/field[@name='state']",
                position="before",
            )
        return view_arch

    @ssi_decorator.insert_on_form_view()
    def _to_insert_queue_cancel_widget_to_form_view(self, view_arch):
        template_xml = "ssi_transaction_queue_cancel_mixin."
        template_xml += "transaction_queue_cancel_form_template"
        if self._queue_to_cancel_insert_form_element_ok:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id=template_xml,
                xpath=self._queue_to_cancel_form_xpath,
                position="after",
            )
        return view_arch

    def _requeue_cancel_job_batch(self):
        self.ensure_one()
        for job in self.cancel_queue_job_ids.filtered(lambda x: x.state != "done"):
            job.requeue()

    def _prepare_queue_cancel_data(self, cancel_reason=False):
        self.ensure_one()
        result = {
            "state": self._queue_to_cancel_state,
            "cancel_reason_id": cancel_reason and cancel_reason.id or False,
        }
        if self._create_sequence_state == self._queue_to_cancel_state:
            self._create_sequence()
        return result

    def _run_pre_queue_cancel_check(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_pre_queue_cancel_check"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_post_queue_cancel_check(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_post_queue_cancel_check"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_pre_queue_cancel_action(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_pre_queue_cancel_action"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_post_queue_cancel_action(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_post_queue_cancel_action"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _recompute_queue_cancel_result(self):
        self.ensure_one()
        self.cancel_queue_job_batch_id.enqueue()
        if self.cancel_queue_job_batch_state == "finished":
            self.with_context(bypass_policy_check=True).action_cancel(
                self.cancel_reason_id
            )

    def _set_cancel_if_no_job(self):
        self.ensure_one()
        if not self.cancel_queue_job_ids:
            self.with_context(bypass_policy_check=True).action_cancel(
                self.cancel_reason_id
            )

    def _check_queue_cancel_policy(self):
        self.ensure_one()

        if not self._automatically_insert_queue_cancel_button:
            return True

        if self.env.context.get("bypass_policy_check", False):
            return True

        if not self.queue_cancel_ok:
            error_message = """
                Document Type: %s
                Context: Start Cancel's Queue Job
                Database ID: %s
                Problem: Document is not allowed to start cancel queue job
                Solution: Check queue cancel policy prerequisite
                """ % (
                self._description.lower(),
                self.id,
            )
            raise UserError(_(error_message))

    def _create_job_batch_cancel(self):
        self.ensure_one()
        str_group = "%s Cancel Batch for ID %s" % (self._description, self.id)
        batch = self.env["queue.job.batch"].get_new_batch(str_group)
        self.write(
            {
                "cancel_queue_job_batch_id": batch.id,
            }
        )
