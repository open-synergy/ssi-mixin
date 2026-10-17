// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_ai_trace_mixin.helpers", function () {
    "use strict";

    var SNIPPET_LENGTH = 160;

    /**
     * Pick the Ace mode and the text to show for one entry field.
     *
     * ``prompt`` and ``result`` use ``markdown``. ``action`` uses ``json``
     * with a two-space pretty-print, and falls back to ``text`` with the
     * raw value when it is not valid JSON.
     *
     * @param {String} fieldName one of prompt, action, result.
     * @param {String} value the raw field value.
     * @returns {Object} an object with the keys ``mode`` and ``text``.
     */
    function pickAceMode(fieldName, value) {
        var text = value || "";
        if (fieldName !== "action") {
            return {mode: "markdown", text: text};
        }
        try {
            return {mode: "json", text: JSON.stringify(JSON.parse(text), null, 2)};
        } catch (error) {
            return {mode: "text", text: text};
        }
    }

    /**
     * Group entries, already sorted, by calendar day.
     *
     * Consecutive entries sharing the same day key end up in the same
     * group, so the input order is preserved.
     *
     * @param {Array} entries the entries, newest first.
     * @param {Function} dayKey maps an entry to its day label.
     * @returns {Array} list of ``{day: String, entries: Array}``.
     */
    function groupByDate(entries, dayKey) {
        var groups = [];
        entries.forEach(function (entry) {
            var day = dayKey(entry);
            var last = groups[groups.length - 1];
            if (last && last.day === day) {
                last.entries.push(entry);
            } else {
                groups.push({day: day, entries: [entry]});
            }
        });
        return groups;
    }

    /**
     * Build the plain text excerpt shown while an entry is closed.
     *
     * @param {String} text the prompt or the result.
     * @returns {String} white space collapsed, at most 160 characters.
     */
    function makeSnippet(text) {
        return (text || "")
            .split(/\s+/)
            .filter(Boolean)
            .join(" ")
            .slice(0, SNIPPET_LENGTH);
    }

    return {
        pickAceMode: pickAceMode,
        groupByDate: groupByDate,
        makeSnippet: makeSnippet,
        SNIPPET_LENGTH: SNIPPET_LENGTH,
    };
});
