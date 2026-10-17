# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import logging
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

TEXT_LIMIT = 16384
TRUNCATED_SUFFIX = "\n…[truncated]"
TEXT_FIELDS = ("prompt", "action", "result")
PURGE_CHUNK = 1000
RETENTION_PARAM = "ssi_ai_trace_mixin.retention_days"
UNIQUE_KEY_FIELDS = ("model", "res_id", "session_key", "turn", "kind")


class AiTrace(models.Model):
    """
    Stores one AI trace entry attached to any document of any model.

    Entries live outside the chatter on purpose: their volume would bloat
    ``mail_message``, a wrong subtype would notify followers (clients
    included) and the portal exposes the chatter of some documents. The
    document is referenced by ``model`` / ``res_id`` and entries are written
    through the idempotent ``ai_trace_append`` API.
    """

    _name = "ai_trace"
    _description = "AI Trace"
    _order = "date desc, id desc"

    model_id = fields.Many2one(
        string="Referenced Model",
        comodel_name="ir.model",
        required=True,
        ondelete="cascade",
        index=True,
        help="Model of the document this entry belongs to.",
    )
    model = fields.Char(
        string="Model Name",
        related="model_id.model",
        store=True,
        index=True,
        help="Technical name of the model of the referenced document.",
    )
    res_id = fields.Many2oneReference(
        string="Document ID",
        model_field="model",
        required=True,
        index=True,
        help="Identifier of the referenced document.",
    )
    session_key = fields.Char(
        string="Session Key",
        size=128,
        required=True,
        help="Free text identifying the AI session that wrote the entry. "
        "It is stored as is and never parsed or validated.",
    )
    turn = fields.Integer(
        string="Turn",
        required=True,
        default=0,
        help="Turn number inside the session. For kinds other than Turn it "
        "is the sequence number of the entry inside the (session, kind) "
        "pair; a Summary always has turn 0.",
    )
    kind = fields.Selection(
        string="Kind",
        selection=[
            ("turn", "Turn"),
            ("summary", "Summary"),
            ("note", "Note"),
            ("policy", "Policy"),
            ("evidence", "Evidence"),
            ("deviation", "Deviation"),
            ("channel", "Channel"),
        ],
        required=True,
        help="Type of the entry. Summary entries are pinned on top of the "
        "timeline and are never purged by the retention cron.",
    )
    prompt = fields.Text(
        string="Prompt",
        help="What the AI was asked, written in markdown.",
    )
    action = fields.Text(
        string="Action",
        help="What the AI did, usually a JSON document.",
    )
    result = fields.Text(
        string="Result",
        help="Outcome reported by the AI, written in markdown.",
    )
    date = fields.Datetime(
        string="Date",
        required=True,
        default=lambda self: fields.Datetime.now(),
        help="Moment the entry happened.",
    )
    user_id = fields.Many2one(
        string="User",
        comodel_name="res.users",
        default=lambda self: self.env.user,
        help="User account that wrote the entry.",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company,
        help="Company of the referenced document, used by the "
        "multi-company record rule.",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        help="Inactive entries are hidden but still count for uniqueness.",
    )
    snippet = fields.Char(
        string="Snippet",
        compute="_compute_snippet",
        help="Plain text excerpt of the prompt or the result, at most 160 "
        "characters, with line breaks replaced by spaces.",
    )

    @api.depends("prompt", "result")
    def _compute_snippet(self):
        """Build a one-line plain text excerpt of the entry.

        The prompt is used when it is set, otherwise the result. White
        space runs, line breaks included, collapse to a single space and
        the excerpt is cut to 160 characters.
        """
        for record in self:
            text = record.prompt or record.result or ""
            record.snippet = " ".join(text.split())[:160]

    def init(self):
        """Create the composite index used to list the entries of a document."""
        self.env.cr.execute(
            "SELECT indexname FROM pg_indexes WHERE indexname = %s",
            ("ai_trace_model_res_id_date_idx",),
        )
        if not self.env.cr.fetchone():
            self.env.cr.execute(
                "CREATE INDEX ai_trace_model_res_id_date_idx "
                "ON ai_trace (model, res_id, date)"
            )

    @api.constrains(*UNIQUE_KEY_FIELDS)
    def _check_unique_key(self):
        """Reject a second entry with the same uniqueness key.

        The key is (``model``, ``res_id``, ``session_key``, ``turn``,
        ``kind``). Inactive entries are part of the check.

        :raises ValidationError: when another entry has the same key
        """
        for record in self:
            duplicate = self.with_context(active_test=False).search_count(
                [
                    ("id", "!=", record.id),
                    ("model", "=", record.model),
                    ("res_id", "=", record.res_id),
                    ("session_key", "=", record.session_key),
                    ("turn", "=", record.turn),
                    ("kind", "=", record.kind),
                ]
            )
            if duplicate:
                raise ValidationError(
                    _(
                        "An AI trace entry already exists for document "
                        "%s,%s, session %s, kind %s, turn %s."
                    )
                    % (
                        record.model,
                        record.res_id,
                        record.session_key,
                        record.kind,
                        record.turn,
                    )
                )

    @api.model
    def _truncate_vals(self, vals):
        """Cut the long text fields of ``vals`` to the storage limit.

        :param dict vals: values about to be written
        :return: tuple ``(vals, overflow)``, where ``vals`` is a copy with
            the long texts cut (suffix included in the limit) and
            ``overflow`` maps each cut field name to its full text
        """
        vals = dict(vals)
        overflow = {}
        for name in TEXT_FIELDS:
            text = vals.get(name)
            if text and len(text) > TEXT_LIMIT:
                overflow[name] = text
                keep = TEXT_LIMIT - len(TRUNCATED_SUFFIX)
                vals[name] = text[:keep] + TRUNCATED_SUFFIX
        return vals, overflow

    def _store_full_text(self, overflow):
        """Keep the full text of cut fields as attachments of the entry.

        An attachment named ``<field>.txt`` already stored for the entry
        is replaced.

        :param dict overflow: field name mapped to its full text
        """
        self.ensure_one()
        Attachment = self.env["ir.attachment"].sudo()
        for name, text in overflow.items():
            filename = "%s.txt" % name
            Attachment.search(
                [
                    ("res_model", "=", self._name),
                    ("res_id", "=", self.id),
                    ("name", "=", filename),
                ]
            ).unlink()
            Attachment.create(
                {
                    "name": filename,
                    "res_model": self._name,
                    "res_id": self.id,
                    "type": "binary",
                    "mimetype": "text/plain",
                    "datas": base64.b64encode(text.encode("utf-8")),
                }
            )

    @api.model_create_multi
    def create(self, vals_list):
        """Create entries, cutting texts longer than 16,384 characters.

        The cut texts are kept whole as ``ir.attachment`` records so that
        a long entry never fails a whole batch.

        :param list vals_list: values of the entries to create
        :return: the created entries
        """
        prepared = [self._truncate_vals(vals) for vals in vals_list]
        records = super().create([vals for vals, _overflow in prepared])
        for record, (_vals, overflow) in zip(records, prepared):
            if overflow:
                record._store_full_text(overflow)
        return records

    def write(self, vals):
        """Update entries, cutting texts longer than 16,384 characters.

        :param dict vals: values to write
        :return: ``True``
        """
        cut_vals, overflow = self._truncate_vals(vals)
        result = super().write(cut_vals)
        if overflow:
            for record in self:
                record._store_full_text(overflow)
        return result

    @api.model
    def _ai_trace_entry_key(self, entry):
        """Return the uniqueness key tuple of an API entry.

        :param dict entry: entry given to ``ai_trace_append``
        :return: tuple (model, res_id, session_key, turn, kind)
        """
        return (
            entry["model"],
            int(entry["res_id"]),
            entry["session_key"],
            int(entry["turn"]),
            entry["kind"],
        )

    @api.model
    def _ai_trace_validate_entries(self, entries):
        """Check the shape and the target document of every entry.

        :param list entries: entries given to ``ai_trace_append``
        :raises ValidationError: when a key is missing, the model is not in
            the registry, or the document does not exist
        """
        required = ("model", "res_id", "session_key", "turn", "kind")
        ids_by_model = {}
        for entry in entries:
            for name in required:
                if entry.get(name) in (None, False, "") and name != "turn":
                    raise ValidationError(
                        _("AI trace entry misses the key '%s'.") % name
                    )
            if entry.get("turn") is None:
                raise ValidationError(_("AI trace entry misses the key 'turn'."))
            if entry["model"] not in self.env:
                raise ValidationError(
                    _("Unknown model '%s' in AI trace entry.") % entry["model"]
                )
            ids_by_model.setdefault(entry["model"], set()).add(int(entry["res_id"]))
        for model, res_ids in ids_by_model.items():
            existing = set(self.env[model].browse(list(res_ids)).exists().ids)
            missing = res_ids - existing
            if missing:
                raise ValidationError(
                    _("Document(s) %s of model '%s' do not exist.")
                    % (sorted(missing), model)
                )

    @api.model
    def _ai_trace_company(self, model, res_id):
        """Return the company an entry of a document belongs to.

        :param str model: technical model name
        :param int res_id: document identifier
        :return: ``res.company`` of the document when the model has a
            ``company_id`` set on it, otherwise the current company
        """
        record = self.env[model].browse(res_id)
        if "company_id" in record._fields and record.company_id:
            return record.company_id
        return self.env.company

    @api.model
    def ai_trace_append(self, entries):
        """Create or update AI trace entries in one idempotent call.

        Public API called through ``call_method`` of muk_rest or MCP.
        Each entry is a dict with the keys ``model``, ``res_id``,
        ``session_key``, ``turn``, ``kind``, ``prompt``, ``action``,
        ``result`` and the optional ``date``. An entry whose uniqueness key
        (model, res_id, session_key, turn, kind) already exists updates
        that record, any other entry creates a new one. One ``search``
        serves the whole batch. A Summary is always stored with turn 0.

        :param list entries: list of entry dicts
        :return: list of ``ai_trace`` ids in the order of ``entries``
        :raises ValidationError: when the model is unknown or the document
            does not exist
        """
        entries = [dict(entry) for entry in entries]
        for entry in entries:
            if entry.get("kind") == "summary":
                entry["turn"] = 0
        self._ai_trace_validate_entries(entries)
        ordered_keys = []
        merged = {}
        for entry in entries:
            key = self._ai_trace_entry_key(entry)
            ordered_keys.append(key)
            vals = merged.setdefault(key, {})
            for name in TEXT_FIELDS + ("date",):
                if entry.get(name) is not None:
                    vals[name] = entry[name]
        existing = {}
        if merged:
            found = self.with_context(active_test=False).search(
                [
                    ("model", "in", list({key[0] for key in merged})),
                    ("res_id", "in", list({key[1] for key in merged})),
                    ("session_key", "in", list({key[2] for key in merged})),
                    ("turn", "in", list({key[3] for key in merged})),
                    ("kind", "in", list({key[4] for key in merged})),
                ]
            )
            for record in found:
                key = (
                    record.model,
                    record.res_id,
                    record.session_key,
                    record.turn,
                    record.kind,
                )
                if key in merged:
                    existing[key] = record
        to_create = []
        create_keys = []
        for key, vals in merged.items():
            if key in existing:
                if vals:
                    existing[key].write(vals)
                continue
            model, res_id, session_key, turn, kind = key
            create_vals = dict(vals)
            create_vals.update(
                {
                    "model_id": self.env["ir.model"]._get(model).id,
                    "res_id": res_id,
                    "session_key": session_key,
                    "turn": turn,
                    "kind": kind,
                    "company_id": self._ai_trace_company(model, res_id).id,
                }
            )
            to_create.append(create_vals)
            create_keys.append(key)
        created = self.create(to_create) if to_create else self.browse()
        records = dict(existing)
        records.update(zip(create_keys, created))
        return [records[key].id for key in ordered_keys]

    @api.model
    def _cron_purge_ai_trace(self):
        """Delete the entries older than the retention period.

        The period is the system parameter
        ``ssi_ai_trace_mixin.retention_days``. ``0`` keeps everything.
        Summary entries are never deleted. Inactive entries are deleted
        too, in chunks of 1,000 records until none is left.
        """
        value = self.env["ir.config_parameter"].sudo().get_param(RETENTION_PARAM, "0")
        try:
            days = int(value)
        except ValueError:
            _logger.warning(
                "Invalid %s value %r, purge skipped.", RETENTION_PARAM, value
            )
            return
        if days <= 0:
            return
        limit_date = fields.Datetime.now() - timedelta(days=days)
        domain = [("kind", "!=", "summary"), ("date", "<", limit_date)]
        Trace = self.with_context(active_test=False)
        records = Trace.search(domain, limit=PURGE_CHUNK)
        while records:
            records.unlink()
            records = Trace.search(domain, limit=PURGE_CHUNK)
