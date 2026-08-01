# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import io
import logging
from base64 import b64encode

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator

_logger = logging.getLogger(__name__)

try:
    import qrcode
except (ImportError, IOError) as err:
    _logger.debug(err)


class MixinQRCode(models.AbstractModel):
    """
    Abstract mixin that adds a computed QR-code image (``qr_image``) to any
    model.

    The QR content is determined per-model via ``ir.model`` configuration:
    if no custom content policy is found the mixin falls back to
    ``_get_qr_standard_content`` which encodes the full web URL of the record.

    Inherits ``mixin.decorator`` so that the QR-code page can be injected into
    the form view automatically when ``_qr_code_create_page`` is ``True``.
    """

    _name = "mixin.qr_code"
    _inherit = [
        "mixin.decorator",
    ]
    _description = "QR Code Mixin"

    _qr_code_create_page = False
    _qr_code_page_xpath = "//page[last()]"

    def _compute_qr_image(self):
        """Render the QR-code PNG image of every record.

        No ``@api.depends``: the QR content is produced by the
        free-form ``qr_python_code`` defined on ``ir.model``, which
        may read any field on the document, so the set of
        dependencies cannot be declared statically. This falls under
        the "called outside the dependency engine" exception for
        compute methods without ``@api.depends``. The field stays
        ``store=False`` for the same reason: a stored value could
        never be reliably invalidated when ``qr_python_code``
        changes.

        :return: nothing; assigns ``qr_image``
        """
        ir_model = self.env["ir.model"].search(self._get_qr_code_content_criteria())
        for document in self:
            result = False
            content = document._get_qr_code_content(ir_model=ir_model)
            if content:
                try:
                    img = qrcode.make(content)
                    buffer = io.BytesIO()
                    img.save(buffer, format="PNG")
                    buffer.seek(0)
                    result = b64encode(buffer.read()).decode("ascii")
                except Exception:  # pylint: disable=broad-except
                    result = False
            document.qr_image = result

    qr_image = fields.Binary(
        string="QR Code",
        compute="_compute_qr_image",
        store=False,
    )

    @ssi_decorator.insert_on_form_view()
    def _qr_code_insert_form_element(self, view_arch):
        """Insert the QR-code page into the form view.

        Runs through the ``insert_on_form_view`` decorator hook, and
        only adds the page when ``_qr_code_create_page`` is ``True``
        on the inheriting model.

        :param view_arch: the form view architecture being extended
        :return: the (possibly modified) view architecture
        """
        if self._qr_code_create_page:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id="ssi_qr_code_mixin.qr_code_page",
                xpath=self._qr_code_page_xpath,
                position="after",
            )
        return view_arch

    def _get_qr_code_content(self, ir_model=None):
        """Resolve the QR content configured for this document.

        Extension point: override to change how the content policy
        is resolved.

        :param ir_model: optional ``ir.model`` recordset already
            located by the caller with ``_get_qr_code_content_criteria``
            (avoids repeating the same search for every document in a
            batch compute). When omitted, this method performs the
            search itself, keeping the previous no-argument signature
            working for external callers.
        :return: the QR content, as returned by
            ``ir.model._get_qr_content`` or ``_get_qr_standard_content``
        """
        self.ensure_one()
        if ir_model is None:
            ir_model = self.env["ir.model"].search(self._get_qr_code_content_criteria())
        if ir_model:
            content = ir_model[0]._get_qr_content(self)
        else:
            content = self._get_qr_standard_content()
        return content

    def _get_qr_code_content_criteria(self):
        """Build the domain selecting the ``ir.model`` of this model.

        Extension point: override to widen or narrow which
        ``ir.model`` record supplies the QR content configuration.

        :return: an Odoo search domain
        """
        return [
            ("model", "=", self._name),
        ]

    def _get_qr_standard_content(self):
        """Build the standard QR content: the backend URL of this document.

        :return: the full backend URL of this record, as a string
        """
        self.ensure_one()
        odoo_url = self.env["ir.config_parameter"].get_param("web.base.url")
        document_url = "/web?#id=%d&view_type=form&model=%s" % (
            self.id,
            self._name,
        )
        full_url = odoo_url + document_url
        return full_url
