# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class MixinDataRequirement(models.AbstractModel):
    """
    Abstract mixin that adds data-requirement tracking capabilities to any
    transactional model.

    Inheriting models gain a ``data_requirement_ids`` One2many that surfaces
    outstanding data requirements linked to the current record, together with
    an optional automatically injected view page (controlled by a class-level
    flag) so users can submit fulfilment data directly from the parent form.
    """

    _name = "mixin.data_requirement"
    _inherit = [
        "mixin.decorator",
    ]
    _description = "Data Requirement Mixin"

    _data_requirement_create_filter = False
    _data_requirement_filter_xpath = "//field[last()]"

    _data_requirement_create_page = False
    _data_requirement_page_xpath = "//page[last()]"

    _data_requirement_configurator_field_name = False
    _data_requirement_partner_field_name = False
    _data_requirement_contact_field_name = False

    data_requirement_document_ids = fields.One2many(
        string="Data Requirements",
        comodel_name="data_requirement.document",
        inverse_name="res_id",
        domain=lambda self: [("res_model", "=", self._name)],
        auto_join=True,
    )
    data_requirement_status = fields.Selection(
        string="Data Requirement Status",
        selection=[
            ("not_needed", "Not Needed"),
            ("open", "In Progress"),
            ("done", "Done"),
        ],
        compute="_compute_data_requirement_status",
        store=True,
    )
    allowed_partner_id = fields.Many2one(
        string="Allowed Partner",
        comodel_name="res.partner",
        compute="_compute_allowed_partner_id",
        store=False,
    )

    def _compute_allowed_partner_id(self):
        for record in self:
            result = False

            if self._data_requirement_partner_field_name and hasattr(
                record, self._data_requirement_partner_field_name
            ):
                result = getattr(record, self._data_requirement_partner_field_name)
                if result:
                    result = result.commercial_partner_id

            record.allowed_partner_id = result

    @api.depends(
        "data_requirement_document_ids",
        "data_requirement_document_ids.data_requirement_id",
        "data_requirement_document_ids.data_requirement_id.state",
    )
    def _compute_data_requirement_status(self):
        for record in self:
            result = "not_needed"
            drs = record.data_requirement_document_ids.mapped("data_requirement_id")
            num_of_data_requirement = len(drs)
            num_of_done_data_requirement = len(
                drs.filtered(lambda r: r.state == "done")
            )

            if (  # pylint: disable=consider-using-in
                num_of_data_requirement != 0
                and num_of_data_requirement != num_of_done_data_requirement
            ):
                result = "open"
            elif (
                num_of_data_requirement != 0
                and num_of_data_requirement == num_of_done_data_requirement
            ):
                result = "done"

            record.data_requirement_status = result

    @ssi_decorator.insert_on_search_view()
    def _data_requirement_insert_search_element(self, view_arch):
        if self._data_requirement_create_filter:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id="ssi_data_requirement_mixin.data_requirement_filter",
                xpath=self._data_requirement_filter_xpath,
                position="after",
            )
        return view_arch

    @ssi_decorator.insert_on_form_view()
    def _data_requirement_insert_form_element(self, view_arch):
        if self._data_requirement_create_page:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id="ssi_data_requirement_mixin.data_requirement",
                xpath=self._data_requirement_page_xpath,
                position="after",
            )
        return view_arch

    def action_create_data_requirement(self):
        for record in self.sudo():
            record._create_data_requirement()

    def action_open_data_requirement(self):
        for record in self.sudo():
            result = record._open_data_requirement()
        return result

    def action_add_data_requirement(self):
        for record in self.sudo():
            result = record._add_data_requirement()
        return result

    def _add_data_requirement(self):
        self.ensure_one()
        waction = self.env.ref(
            "ssi_data_requirement_mixin.add_data_requirement_action"
        ).read()[0]
        return waction

    def _open_data_requirement(self):
        self.ensure_one()
        waction = self.env.ref(
            "ssi_data_requirement_mixin.data_requirement_action"
        ).read()[0]
        dr_ids = self.data_requirement_document_ids.mapped("data_requirement_id").ids
        waction.update(
            {
                "domain": [("id", "in", dr_ids)],
            }
        )
        return waction

    def _data_requirement_get_partner(self):
        self.ensure_one()

        if not self._data_requirement_partner_field_name:
            return False

        if not hasattr(self, self._data_requirement_partner_field_name):
            return False

        return getattr(self, self._data_requirement_partner_field_name)

    def _data_requirement_get_contact(self):
        self.ensure_one()

        if not self._data_requirement_contact_field_name:
            return False

        if not hasattr(self, self._data_requirement_contact_field_name):
            return False

        return getattr(self, self._data_requirement_contact_field_name)

    # pylint: disable=inconsistent-return-statements
    def _create_data_requirement(
        self,
    ):
        self.ensure_one()
        if not hasattr(self, self._data_requirement_configurator_field_name):
            return True

        configurator = getattr(self, self._data_requirement_configurator_field_name)

        for data_requirement in configurator.data_requirement_ids:
            partner = self._data_requirement_get_partner()
            contact = self._data_requirement_get_contact()

            dr = self.env["data_requirement"].create(
                {
                    "type_id": data_requirement.type_id.id,
                    "partner_id": partner and partner.id or False,
                    "contact_partner_id": contact and contact.id or False,
                    "date": fields.Date.today(),
                    "date_commitment": fields.Date.today(),
                    "mode": data_requirement.type_id.mode,
                    "title": data_requirement.title or data_requirement.type_id.name,
                    "instruction_url": data_requirement.type_id.instruction_url,
                }
            )

            self.env["data_requirement.document"].create(
                {
                    "res_id": self.id,
                    "res_model": self._name,
                    "data_requirement_id": dr.id,
                }
            )
