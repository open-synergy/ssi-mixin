# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models

from odoo.addons.ssi_decorator import ssi_decorator


class MixinTransactionQueue(models.AbstractModel):
    _name = "mixin.transaction_queue"
    _inherit = [
        "mixin.transaction",
    ]
    _description = "Transaction + Queue Mixin"
    _queue_processing_create_page = False
    _queue_processing_page_xpath = "//page[last()]"

    @ssi_decorator.insert_on_form_view()
    def _reference_document_insert_form_element(self, view_arch):
        if self._queue_processing_create_page:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id="ssi_transaction_queue_mixin.queue",
                xpath=self._queue_processing_page_xpath,
                position="after",
            )
        return view_arch
