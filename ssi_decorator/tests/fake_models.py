# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Throwaway model exercising ``mixin.decorator`` for the unit test suite.

DELIBERATELY NOT IMPORTED FROM ``tests/__init__.py``, and not imported at
the top of ``tests/test_ssi_decorator.py`` either. Odoo builds every model
class it sees while an addon loads, so importing this module there would
turn ``test_decorator`` into a real model with a real table in every
database that installs ``ssi_decorator``. The ``fake_models:`` key in
``tests/test_data_ssi_decorator.yaml`` imports it at the right moment
instead, via ``odoo_yaml_test.YamlTransactionCase.run_yaml_scenario``.
"""

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class TestDecorator(models.Model):
    """Concrete consumer of ``mixin.decorator``, alive only in a test.

    Carries the decorator-marked methods that ``mixin.decorator``
    discovers via introspection, so the mixin's dispatch logic
    (``_get_view`` calling ``_run_insert_on_form_view`` calling
    ``_add_view_element``, and the ``_pre_confirm_check`` marker other
    mixins look for) has a concrete model to run against.
    """

    _name = "test_decorator"
    _description = "Test Decorator"
    _inherit = [
        "mixin.decorator",
    ]

    name = fields.Char(
        string="Name",
        required=True,
        help="Free-text label used only to create a record to exercise "
        "the mixin's decorator dispatch with.",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Confirmed"),
        ],
        default="draft",
        help="Kept only because the form view the test builds needs a "
        "field to declare a statusbar header for; ``mixin.decorator`` "
        "itself never reads this field.",
    )

    @ssi_decorator.insert_on_form_view()
    def _test_decorator_insert_form_element(self, view_arch):
        """Insert the test's QWeb fragment into the form view arch.

        The fragment lives in an ``ir.ui.view`` the test creates at
        runtime (fake models ship no view XML of their own), so it is
        looked up by its ``key`` instead of a static XML ID.

        :param view_arch: Form view architecture being built.
        :type view_arch: etree._Element
        :return: The architecture, with the fragment inserted after
            ``//page[@name='page_note']`` when the runtime QWeb view
            exists; unchanged otherwise.
        :rtype: etree._Element
        """
        qweb_view = self.env["ir.ui.view"].search(
            [
                ("type", "=", "qweb"),
                ("key", "=", "test_decorator.test_decorator_page"),
            ],
            limit=1,
        )
        if not qweb_view:
            return view_arch
        return self._add_view_element(
            view_arch=view_arch,
            qweb_template_xml_id=qweb_view.id,
            xpath="//page[@name='page_note']",
            position="after",
        )

    @ssi_decorator.pre_confirm_check("test_decorator_marker")
    def _test_decorator_pre_confirm_check(self):
        """Exist only so its ``_pre_confirm_check`` marker is assertable.

        Not called by ``ssi_decorator`` itself - consumers such as
        ``ssi_transaction_mixin`` are the ones that actually invoke
        methods carrying this marker.
        """
