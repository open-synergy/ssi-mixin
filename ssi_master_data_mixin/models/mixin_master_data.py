# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MixinMasterData(models.AbstractModel):
    """Abstract mixin for master data (reference data) models.

    Provides a reusable base for master/reference data records with
    standard fields (``name``, ``code``, ``active``, ``note``), automatic
    sequence generation, chatter integration, and print-document support.

    Class-level attributes that concrete models may override:

    * ``_field_name_string`` – Human-readable label for the ``name`` field.
      Defaults to ``"Name"``.
    * ``_show_code_on_display_name`` – When ``True`` the display name is
      rendered as ``[code] name``.  Defaults to ``False``.
    * ``_automatically_insert_print_button`` – Auto-inject a print button
      into the form header.  Defaults to ``True``.
    * ``_print_button_xpath`` – XPath location for the injected print button.
      Defaults to ``"/form/header"``.
    * ``_print_button_position`` – Insertion position for the print button.
      Defaults to ``"inside"``.
    """

    _name = "mixin.master_data"
    _inherit = [
        "mail.activity.mixin",
        "mail.thread",
        "mixin.print_document",
        "mixin.sequence",
    ]
    _description = "Mixin for Master Data"
    _field_name_string = "Name"
    _show_code_on_display_name = False
    _automatically_insert_print_button = True
    _print_button_xpath = "/form/header"
    _print_button_position = "inside"

    @api.model
    def _get_field_name_string(self):
        """Return the label string for the ``name`` field.

        Reads :attr:`_field_name_string` so that concrete models can
        customise the field label without re-declaring the field itself.

        :return: Field label string.
        :rtype: str
        """
        return self._field_name_string

    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
        help="""Master data unique identifier.

* Fill with '/' if You do not need unique identifier
* Click 'Generate Code' button to automatically assign code.
  Sequence template mush be set to perform this action
  Only master data with '/' code will be assign automatic code""",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        help="""Master data status

* Inactive data can not be selected when creating new transaction
* Transaction with inactive master data can still be viewed
* Set master data as inactive if master data no longger needed,
but master data already used on transaction""",
    )
    note = fields.Text(
        string="Note",
    )

    def copy(self, default=None):
        """Duplicate the record, appending ``(copy)`` to the ``code`` field.

        Overrides the standard ``copy`` to prevent the duplicated record
        from violating the unique-code constraint by suffixing the
        original code with ``(copy)``.

        :param dict default: Field values to override on the new record.
        :return: The newly created duplicate record.
        :rtype: :class:`MixinMasterData`
        """
        self.ensure_one()
        if default is None:
            default = {}
        if "code" not in default:
            default["code"] = _("%s (copy)", self.code)
        return super().copy(default=default)

    @api.constrains("code")
    def _check_duplicate_code(self):
        """Validate that no two records share the same non-slash ``code``.

        Raises a :class:`~odoo.exceptions.UserError` when a duplicate code
        is detected, excluding records whose code is ``'/'``.

        :raises UserError: If another record with the same ``code`` exists.
        """
        for record in self:
            criteria = [
                ("code", "=", record.code),
                ("id", "!=", record.id),
                ("code", "!=", "/"),
            ]
            count_duplicate = self.search_count(criteria)
            if count_duplicate > 0:
                error_message = f"""
                Document Type: {self._description.lower()}
                Context: Create or update document
                Database ID: {self.id}
                Problem: Dupilicate code
                Solution: Change code
                """
                raise UserError(error_message)

    def action_generate_code(self):
        """Generate and assign a sequence-based code to each selected record.

        Delegates to :meth:`~mixin.sequence._create_sequence` provided by
        ``ssi_sequence_mixin``.  Only records whose current ``code`` is
        ``'/'`` will receive a new code from the configured sequence template.
        """
        for record in self.sudo():
            record._create_sequence()

    def action_reset_code(self):
        """Reset the ``code`` field back to ``'/'`` for each selected record.

        Marks the record as eligible for automatic code generation the next
        time :meth:`action_generate_code` is called.
        """
        for record in self.sudo():
            record.write(
                {
                    "code": "/",
                }
            )

    @api.depends("name", "code")
    def _compute_display_name(self):
        """Compute the display name for each record.

        When :attr:`_show_code_on_display_name` is ``True`` the display name
        is formatted as ``[code] name``; otherwise only ``name`` is used.
        """
        for record in self:
            if record._show_code_on_display_name:
                record.display_name = f"[{record.code}] {record.name}"
            else:
                record.display_name = record.name
