# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class BackendMixin(models.AbstractModel):
    """
    Abstract mixin for *backend configuration* records — singleton-like master
    objects (e.g. accounting settings, HR parameters) that are scoped to a
    company and can be toggled between ``draft`` and ``running`` states.

    Inherits ``mixin.master_data`` and adds:

    * A mandatory ``company_id`` field.
    * A ``state`` selection (``draft`` / ``running``).
    * ``action_running`` — activates this record as the running backend for the
      current company (and deactivates any previously running record).
    * ``action_restart`` — reverts the record to ``draft`` and clears the
      company pointer.

    Subclasses set ``_backend_company_field`` to the name of the field on
    ``res.company`` that should point to the currently active backend record.
    """

    _name = "backend_mixin"
    _inherit = ["mixin.master_data"]
    _description = "Mixin for Backend"

    _backend_company_field = ""
    _automatically_insert_print_button = False

    @api.model
    def _default_company_id(self):
        return self.env.company.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
        copy=True,
    )

    code = fields.Char(
        default="/",
    )

    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("running", "Running"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )

    def _check_company_backend_field(self):
        self.ensure_one()
        result = False
        company_fields = self.env.company._fields
        backend_field = self._backend_company_field

        if backend_field in company_fields:
            result = True
        return result

    def action_running(self):
        for record in self:
            if record._check_company_backend_field():
                check_running_backend_ids = self.search(
                    [
                        ("state", "=", "running"),
                        ("company_id", "=", self.env.company.id),
                        ("id", "!=", record.id),
                    ]
                )
                if check_running_backend_ids:
                    check_running_backend_ids.write({"state": "draft"})
                setattr(
                    self.env.company,
                    self._backend_company_field,
                    record.id,
                )
                record.write({"state": "running"})

    def action_restart(self):
        for record in self:
            if record._check_company_backend_field():
                setattr(
                    self.env.company,
                    self._backend_company_field,
                    False,
                )
                record.write({"state": "draft"})
