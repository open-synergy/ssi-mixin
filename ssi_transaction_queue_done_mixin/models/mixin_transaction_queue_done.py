# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from inspect import getmembers

from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class MixinTransactionQueueDone(models.AbstractModel):
    _name = "mixin.transaction_queue_done"
    _inherit = [
        "mixin.transaction_done",
        "mixin.transaction_queue",
    ]
    _description = "Transaction Mixin - Queue To Done State Mixin"

    _queue_to_done_state = "queue_done"

    # Attributes related to add element on form view automatically
    _automatically_insert_queue_done_policy_fields = True
    _automatically_insert_queue_done_button = True
    _queue_to_done_insert_form_element_ok = False
    _queue_to_done_form_xpath = False

    # Attributes related to add element on search view automatically
    _automatically_insert_queue_done_filter = True

    # Attributes related to add element on tree view automatically
    _automatically_insert_queue_done_state_badge_decorator = True

    state = fields.Selection(
        selection_add=[
            ("queue_done", "Queue To Done"),
            ("done",),
        ],
        ondelete={
            "queue_done": "set default",
        },
    )
    queue_done_ok = fields.Boolean(
        string="Can Start Finished Queue",
        compute="_compute_policy",
        compute_sudo=True,
    )
    done_queue_job_batch_id = fields.Many2one(
        string="To Done Queue Job Batche",
        comodel_name="queue.job.batch",
        readonly=True,
        copy=False,
    )

    done_queue_job_ids = fields.One2many(
        string="To Done Queue Jobs",
        comodel_name="queue.job",
        related="done_queue_job_batch_id.job_ids",
        store=False,
    )
    done_queue_job_batch_state = fields.Selection(
        string="To Done Queue Job Batch State",
        related="done_queue_job_batch_id.state",
        store=True,
    )

    def _compute_policy(self):
        _super = super(MixinTransactionQueueDone, self)
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

    def action_requeue_done(self):
        for record in self.sudo():
            record._requeue_done_job_batch()

    def action_queue_done(self):
        for record in self.sudo():
            record._check_queue_done_policy()
            record._run_pre_queue_done_check()
            record._create_job_batch_done()
            record._run_pre_queue_done_action()
            record.write(record._prepare_queue_done_data())
            record._run_post_queue_done_check()
            record._run_post_queue_done_action()
            record.done_queue_job_batch_id.enqueue()
            record._set_done_if_no_job()

    def action_recompute_queue_done_result(self):
        for record in self.sudo():
            record._recompute_queue_done_result()

    @ssi_decorator.post_done_action()
    def _disconnect_done_batch(self):
        self.ensure_one()

        if not self.done_queue_job_ids:
            self.done_queue_job_batch_id.write(
                {
                    "state": "finished",
                }
            )

        self.write(
            {
                "done_queue_job_batch_id": False,
            }
        )

    @ssi_decorator.insert_on_tree_view()
    def _to_insert_queue_done_button_to_tree_view(self, view_arch):
        template_xml = "ssi_transaction_queue_done_mixin."
        template_xml += "tree_button_queue_done"
        if self._automatically_insert_queue_done_button:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id="ssi_transaction_queue_done_mixin.tree_button_queue_done",
                xpath="/tree/header",
                position="inside",
            )
        return view_arch

    @ssi_decorator.insert_on_tree_view()
    def _to_insert_queue_done_state_badge_decorator(self, view_arch):
        if self._automatically_insert_queue_done_state_badge_decorator:
            _xpath = "/tree/field[@name='state']"
            if len(view_arch.xpath(_xpath)) == 0:
                return view_arch
            node_xpath = view_arch.xpath(_xpath)[0]
            node_xpath.set("decoration-success", "state == 'queue_done'")
        return view_arch

    @ssi_decorator.insert_on_search_view()
    def _to_insert_queue_done_filter_on_search_view(self, view_arch):
        template_xml = "ssi_transaction_queue_done_mixin."
        template_xml += "queue_done_filter"
        if self._automatically_insert_queue_done_filter:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id=template_xml,
                xpath=self._state_filter_xpath,
                position="after",
            )
        view_arch = self._reorder_state_filter_on_search_view(view_arch)
        return view_arch

    @ssi_decorator.insert_on_form_view()
    def _to_insert_queue_done_policy_field_to_form_view(self, view_arch):
        template_xml = "ssi_transaction_queue_done_mixin."
        template_xml += "queue_done_policy_field"
        if self._automatically_insert_queue_done_policy_fields:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id=template_xml,
                xpath=self._policy_field_xpath,
                position="before",
            )
        return view_arch

    @ssi_decorator.insert_on_form_view()
    def _to_insert_queue_done_button_to_form_view(self, view_arch):
        template_xml = "ssi_transaction_queue_done_mixin."
        template_xml += "button_queue_done"
        if self._automatically_insert_queue_done_button:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id=template_xml,
                xpath="/form/header/field[@name='state']",
                position="before",
            )
        return view_arch

    @ssi_decorator.insert_on_form_view()
    def _to_insert_queue_done_widget_to_form_view(self, view_arch):
        template_xml = "ssi_transaction_queue_done_mixin."
        template_xml += "transaction_queue_done_form_template"
        if self._queue_to_done_insert_form_element_ok:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id=template_xml,
                xpath=self._queue_to_done_form_xpath,
                position="after",
            )
        return view_arch

    def _requeue_done_job_batch(self):
        self.ensure_one()
        for job in self.done_queue_job_ids.filtered(lambda x: x.state != "done"):
            job.requeue()

    def _prepare_queue_done_data(self):
        self.ensure_one()
        result = {
            "state": self._queue_to_done_state,
        }
        if self._create_sequence_state == self._queue_to_done_state:
            self._create_sequence()
        return result

    def _run_pre_queue_done_check(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_pre_queue_done_check"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_post_queue_done_check(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_post_queue_done_check"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_pre_queue_done_action(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_pre_queue_done_action"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_post_queue_done_action(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_post_queue_done_action"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _recompute_queue_done_result(self):
        self.ensure_one()
        self.done_queue_job_batch_id.enqueue()
        if self.done_queue_job_batch_state == "finished":
            self.action_done()

    def _set_done_if_no_job(self):
        self.ensure_one()
        if not self.done_queue_job_ids:
            self.action_done()

    def _check_queue_done_policy(self):
        self.ensure_one()

        if not self._automatically_insert_queue_done_button:
            return True

        if self.env.context.get("bypass_policy_check", False):
            return True

        if not self.queue_done_ok:
            error_message = """
                Document Type: %s
                Context: Start Finish's Queue Job
                Database ID: %s
                Problem: Document is not allowed to start finish queue job
                Solution: Check queue finish policy prerequisite
                """ % (
                self._description.lower(),
                self.id,
            )
            raise UserError(_(error_message))

    def _create_job_batch_done(self):
        self.ensure_one()
        str_group = "%s Done Batch for ID %s" % (self._description, self.id)
        batch = self.env["queue.job.batch"].get_new_batch(str_group)
        self.write(
            {
                "done_queue_job_batch_id": batch.id,
            }
        )
