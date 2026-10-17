# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import api, fields, models

CHATTER_XPATH = (
    "//div[contains(concat(' ', normalize-space(@class), ' '), ' oe_chatter ')]"
)


class MixinAiTrace(models.AbstractModel):
    """
    Abstract mixin giving a model the AI trace timeline.

    Models inheriting ``mixin.ai_trace`` gain ``ai_trace_ids`` (the entries
    of ``ai_trace`` written against the record), ``ai_trace_count`` and, on
    every form view that holds a chatter, the hidden count field the web
    client needs to show the ``Chatter | AI Trace (n)`` toggle.
    """

    _name = "mixin.ai_trace"
    _description = "Mixin Object for AI Trace"

    ai_trace_ids = fields.One2many(
        string="AI Traces",
        comodel_name="ai_trace",
        inverse_name="res_id",
        domain=lambda self: [("model", "=", self._name)],
        auto_join=True,
        help="AI trace entries written against this document.",
    )
    ai_trace_count = fields.Integer(
        string="AI Trace Count",
        compute="_compute_ai_trace_count",
        help="Number of active AI trace entries of this document.",
    )

    @api.depends("ai_trace_ids")
    def _compute_ai_trace_count(self):
        """Count the active AI trace entries of each record."""
        for record in self:
            record.ai_trace_count = len(record.ai_trace_ids)

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        """Add the hidden ``ai_trace_count`` field to forms with a chatter.

        The field is the marker the web client looks for to wrap the
        chatter with the ``Chatter | AI Trace (n)`` toggle, so the views of
        the inheriting models never need to be edited.

        :return: the processed view definition
        """
        result = super().fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu,
        )
        if view_type != "form":
            return result
        doc = etree.fromstring(result["arch"].encode("utf-8"))
        chatters = doc.xpath(CHATTER_XPATH)
        if not chatters or doc.xpath("//field[@name='ai_trace_count']"):
            return result
        node = etree.Element(
            "field",
            name="ai_trace_count",
            invisible="1",
            modifiers='{"invisible": true}',
        )
        chatters[0].addprevious(node)
        result["arch"] = etree.tostring(doc, encoding="unicode")
        result["fields"].update(self.fields_get(["ai_trace_count"]))
        return result
