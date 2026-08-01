# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree
from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSsiDecorator(YamlTransactionCase):
    """Scenario tests for the ``mixin.decorator`` dispatch machinery.

    ``mixin.decorator`` is an ``AbstractModel`` and cannot be
    instantiated directly, so this suite exercises it through
    ``test_decorator``, a throwaway model declared in
    ``tests/fake_models.py`` and loaded via the ``fake_models:`` key of
    ``test_data_ssi_decorator.yaml`` - see that module's docstring for
    why it must not be imported here.
    """

    def test_ssi_decorator(self):
        """Run the marker-attachment and missing-template scenarios."""
        self.run_yaml_scenario("test_data_ssi_decorator.yaml")

    def test_insert_on_form_view_arch(self):
        """Assert the arch ``get_view`` returns carries the fragment.

        Pure Python - trigger P1 (L-01: what is under test is the arch
        *returned* by ``get_view``/``_get_view``, and ``action: call``
        discards a method's return value, so YAML cannot assert it).
        """
        self.run_yaml_scenario("test_data_ssi_decorator.yaml")
        model = self.env["test_decorator"]
        self.env["ir.ui.view"].create(
            {
                "name": "test_decorator_page",
                "key": "test_decorator.test_decorator_page",
                "type": "qweb",
                "arch": (
                    '<t t-name="test_decorator.test_decorator_page">'
                    '<page name="test_decorator_injected_page" '
                    'string="Injected By Decorator">'
                    '<field name="name"/>'
                    "</page>"
                    "</t>"
                ),
            }
        )
        form_view = self.env["ir.ui.view"].create(
            {
                "name": "test_decorator.form",
                "model": "test_decorator",
                "type": "form",
                "arch": (
                    "<form>"
                    "<header>"
                    '<field name="state" widget="statusbar"/>'
                    "</header>"
                    "<sheet>"
                    "<group>"
                    '<field name="name"/>'
                    "</group>"
                    "<notebook>"
                    '<page name="page_note" string="Notes"/>'
                    "</notebook>"
                    "</sheet>"
                    "</form>"
                ),
            }
        )

        result = model.get_view(view_id=form_view.id, view_type="form")

        self.assertIn("test_decorator_injected_page", result["arch"])

    def test_add_view_element_position(self):
        """Assert ``before``/``inside`` place the fragment correctly.

        Pure Python - trigger P1 (L-01: what is under test is the etree
        ``_add_view_element`` returns, and ``action: call`` discards a
        method's return value, so YAML cannot assert it).
        """
        self.run_yaml_scenario("test_data_ssi_decorator.yaml")
        model = self.env["test_decorator"]
        qweb_view = self.env["ir.ui.view"].create(
            {
                "name": "test_decorator_page",
                "key": "test_decorator.test_decorator_page",
                "type": "qweb",
                "arch": (
                    '<t t-name="test_decorator.test_decorator_page">'
                    '<page name="injected"/>'
                    "</t>"
                ),
            }
        )

        before_arch = etree.XML('<form><group name="target"/></form>')
        before_result = model._add_view_element(
            view_arch=before_arch,
            qweb_template_xml_id=qweb_view.id,
            xpath="//group[@name='target']",
            position="before",
        )
        self.assertEqual(before_result[0].tag, "page")
        self.assertEqual(before_result[1].get("name"), "target")

        inside_arch = etree.XML('<form><group name="target"/></form>')
        inside_result = model._add_view_element(
            view_arch=inside_arch,
            qweb_template_xml_id=qweb_view.id,
            xpath="//group[@name='target']",
            position="inside",
        )
        target_group = inside_result.xpath("//group[@name='target']")[0]
        self.assertEqual(target_group[0].tag, "page")

    def test_add_view_element_missing_xpath_is_noop(self):
        """Assert a missing xpath leaves the arch unchanged.

        Pure Python - trigger P1 (L-01: what is under test is the etree
        ``_add_view_element`` returns, and ``action: call`` discards a
        method's return value, so YAML cannot assert it).
        """
        self.run_yaml_scenario("test_data_ssi_decorator.yaml")
        model = self.env["test_decorator"]
        qweb_view = self.env["ir.ui.view"].create(
            {
                "name": "test_decorator_page",
                "key": "test_decorator.test_decorator_page",
                "type": "qweb",
                "arch": (
                    '<t t-name="test_decorator.test_decorator_page">'
                    '<page name="injected"/>'
                    "</t>"
                ),
            }
        )
        view_arch = etree.XML('<form><group name="left"/></form>')

        result = model._add_view_element(
            view_arch=view_arch,
            qweb_template_xml_id=qweb_view.id,
            xpath="//group[@name='does_not_exist']",
            position="after",
        )

        self.assertEqual(etree.tostring(result), etree.tostring(view_arch))

    def test_insert_on_form_view_without_marker_is_noop(self):
        """Assert the arch is untouched when no method carries a marker.

        Pure Python - trigger P1 (L-01: what is under test is the etree
        ``_run_insert_on_form_view`` returns, and ``action: call``
        discards a method's return value, so YAML cannot assert it).
        Calls the bare ``mixin.decorator`` abstract model, which has no
        decorator-marked methods of its own (``test_decorator`` does,
        but ``_inherit`` does not copy them back onto the mixin).
        """
        self.run_yaml_scenario("test_data_ssi_decorator.yaml")
        mixin = self.env["mixin.decorator"]
        view_arch = etree.XML('<form><group name="left"/></form>')

        result = mixin._run_insert_on_form_view(view_arch)

        self.assertIs(result, view_arch)
