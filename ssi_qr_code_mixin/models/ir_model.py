# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval, test_python_expr


class IrModel(models.Model):
    """
    Extends ``ir.model`` with QR-code content configuration fields.

    Each model can choose to use the standard content (the web URL of the
    record) or supply custom Python code that must assign the desired
    QR string to a local variable ``result``.
    """

    _name = "ir.model"
    _inherit = "ir.model"

    qr_use_standard_content = fields.Boolean(
        string="Use Standard Content",
        default=True,
    )
    qr_python_code = fields.Text(
        string="Python Code for Custom Content",
        default="result = True",
    )

    def _get_qr_localdict(self, document):
        """Build the ``safe_eval`` localdict for ``qr_python_code``.

        :param document: the document the QR code is generated for
        :return: dict exposing ``env`` and ``document``; the custom
            code is expected to assign the content to ``result``
        """
        self.ensure_one()
        return {
            "env": self.env,
            "document": document,
        }

    def _get_qr_content(self, document):
        """Resolve the QR content configured on this ``ir.model`` row.

        :param document: the document the QR code is generated for
        :return: the standard content or the custom content,
            depending on ``qr_use_standard_content``
        """
        self.ensure_one()
        if self.qr_use_standard_content:
            content = document._get_qr_standard_content()
        else:
            content = self._get_qr_custom_content(document)
        return content

    def _get_qr_custom_content(self, document):
        """Evaluate ``qr_python_code`` to build the custom QR content.

        Executes ``qr_python_code`` with ``env`` and ``document`` in
        its localdict, and expects it to assign the QR string to a
        local variable ``result``. Any failure (syntax error, or
        ``result`` never assigned) is swallowed and yields an empty
        string, so the caller can treat it the same as "no content".

        :param document: the document the QR code is generated for
        :return: the custom QR content, or an empty string on
            failure
        """
        self.ensure_one()
        result = ""
        localdict = self._get_qr_localdict(document)
        try:
            safe_eval(self.qr_python_code, localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        except Exception:
            result = ""
        return result

    @api.constrains(
        "qr_python_code",
    )
    def _check_qr_python_code(self):
        """Validate that ``qr_python_code`` is syntactically correct.

        :raises ValidationError: when ``qr_python_code`` cannot be
            compiled as a Python expression
        """
        for action in self.sudo().filtered("qr_python_code"):
            msg = test_python_expr(expr=action.qr_python_code.strip(), mode="exec")
            if msg:
                raise ValidationError(msg)
