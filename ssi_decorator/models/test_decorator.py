# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class TestDecorator(models.Model):
    _name = "test.decorator"
    _description = "Test Decorator"
    _inherit = [
        "mixin.decorator",
    ]

    name = fields.Char(
        string="Name",
        required=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Confirmed"),
        ],
        default="draft",
    )
    test_result = fields.Text(
        string="Test Result",
        help="Scratch field used only by the unit test suite to capture the "
        "outcome of methods whose result cannot be asserted directly (e.g. "
        "the arch returned by fields_view_get, or the arch returned by "
        "_add_view_element), so it can be read back and asserted from a "
        "YAML scenario.",
    )

    @ssi_decorator.insert_on_form_view()
    def _test_decorator_insert_form_element(self, view_arch):
        view_arch = self._add_view_element(
            view_arch=view_arch,
            qweb_template_xml_id="ssi_decorator.test_decorator_page",
            xpath="//page[@name='page_note']",
            position="after",
        )
        return view_arch

    @ssi_decorator.pre_confirm_check("test_decorator_marker")
    def _test_decorator_pre_confirm_check(self):
        """Not called by ssi_decorator itself - it only exists so its
        ``_pre_confirm_check`` marker attribute can be asserted by the unit
        test suite (consumers such as ssi_transaction_mixin are the ones
        that actually invoke methods carrying this marker)."""

    def _test_capture_form_view_arch(self, view_id=False):
        """Call fields_view_get and stash the resulting arch into
        test_result, since a YAML scenario can only assert record fields,
        not a method's return value."""
        self.ensure_one()
        result = self.get_view(view_id=view_id, view_type="form")
        self.test_result = result["arch"]

    def _test_capture_add_view_element_missing_xpath(self):
        """Prove _add_view_element's early-return branch: when the xpath is
        not found in the arch, the arch is returned unmodified. Calls
        _add_view_element directly with a hand-built arch that does not
        contain the target xpath, and stashes the (unchanged) result into
        test_result for assertion."""
        self.ensure_one()
        view_arch = etree.XML('<form><group name="left"/></form>')
        result_arch = self._add_view_element(
            view_arch=view_arch,
            qweb_template_xml_id="ssi_decorator.test_decorator_page",
            xpath="//group[@name='does_not_exist']",
            position="after",
        )
        self.test_result = etree.tostring(result_arch).decode()
