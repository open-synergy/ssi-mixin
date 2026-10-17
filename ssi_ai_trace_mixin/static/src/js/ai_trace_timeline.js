// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_ai_trace_mixin.Timeline", function (require) {
    "use strict";

    var ajax = require("web.ajax");
    var basic_fields = require("web.basic_fields");
    var core = require("web.core");
    var field_utils = require("web.field_utils");
    var Widget = require("web.Widget");
    var helpers = require("ssi_ai_trace_mixin.helpers");

    // Loaded only for its side effect: it adds the markdown and json
    // modes to ``AceEditor.prototype.jsLibs``.
    require("ssi_web_widget_ace_mode.AceEditor");

    var _t = core._t;
    var qweb = core.qweb;

    var PAGE_SIZE = 20;
    var LIST_FIELDS = ["date", "session_key", "turn", "kind", "snippet"];
    var SECTIONS = [
        {name: "prompt", title: _t("Prompt")},
        {name: "action", title: _t("Action")},
        {name: "result", title: _t("Result")},
    ];
    var KIND_LABELS = {
        turn: _t("Turn"),
        summary: _t("Summary"),
        note: _t("Note"),
        policy: _t("Policy"),
        evidence: _t("Evidence"),
        deviation: _t("Deviation"),
        channel: _t("Channel"),
    };

    /**
     * Read-only timeline of the AI trace entries of one document.
     *
     * Summaries are pinned on top, the other entries follow newest first,
     * grouped by day and loaded 20 at a time. Every entry starts closed
     * with a plain text snippet; the Ace viewers are created only when an
     * entry is opened and destroyed when it is closed.
     */
    var Timeline = Widget.extend({
        template: "ssi_ai_trace_mixin.Timeline",
        events: {
            "click .o_ai_trace_entry_header": "_onToggleEntry",
            "click .o_ai_trace_load_older": "_onLoadOlder",
        },

        /**
         * @override
         * @param {Widget} parent the form renderer.
         * @param {Object} options ``model`` and ``resId`` of the document.
         */
        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.model = options.model;
            this.resId = options.resId;
            this._offset = 0;
            this._lastDay = null;
            this._viewers = {};
            this._texts = {};
        },

        /**
         * @override
         */
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                return self._loadSummaries().then(function () {
                    return self._loadPage();
                });
            });
        },

        /**
         * @override
         */
        destroy: function () {
            Object.keys(this._viewers).forEach(this._destroyViewers.bind(this));
            this._super.apply(this, arguments);
        },

        // ----------------------------------------------------------------------
        // Private
        // ----------------------------------------------------------------------

        /**
         * @private
         * @param {String} kindOperator ``=`` for summaries, ``!=`` otherwise.
         * @returns {Array} the search domain of the document entries.
         */
        _domain: function (kindOperator) {
            return [
                ["model", "=", this.model],
                ["res_id", "=", this.resId],
                ["kind", kindOperator, "summary"],
            ];
        },

        /**
         * Add the display fields (day label, time) to a fetched entry.
         *
         * @private
         * @param {Object} entry the record returned by ``search_read``.
         * @returns {Object} the same entry.
         */
        _decorate: function (entry) {
            var moment = field_utils.parse.datetime(
                entry.date,
                {type: "datetime"},
                {isUTC: true}
            );
            entry._day = moment.format("LL");
            entry._time = moment.format("LT");
            return entry;
        },

        /**
         * @private
         * @param {Object} entry a decorated entry.
         * @returns {jQuery} the rendered, closed entry.
         */
        _renderEntry: function (entry) {
            return $(
                qweb.render("ssi_ai_trace_mixin.Entry", {
                    entry: entry,
                    kind_label: KIND_LABELS[entry.kind] || entry.kind,
                })
            );
        },

        /**
         * Load and show every Summary entry of the document.
         *
         * @private
         * @returns {Promise}
         */
        _loadSummaries: function () {
            var self = this;
            return this._rpc({
                model: "ai_trace",
                method: "search_read",
                kwargs: {
                    domain: this._domain("="),
                    fields: LIST_FIELDS,
                    order: "date desc, id desc",
                },
            }).then(function (entries) {
                var $box = self.$(".o_ai_trace_summaries");
                entries.map(self._decorate.bind(self)).forEach(function (entry) {
                    $box.append(self._renderEntry(entry));
                });
                self._hasSummaries = entries.length > 0;
                self._refreshEmpty();
            });
        },

        /**
         * Load the next page of non-summary entries and append it.
         *
         * @private
         * @returns {Promise}
         */
        _loadPage: function () {
            var self = this;
            return this._rpc({
                model: "ai_trace",
                method: "search_read",
                kwargs: {
                    domain: this._domain("!="),
                    fields: LIST_FIELDS,
                    order: "date desc, id desc",
                    limit: PAGE_SIZE + 1,
                    offset: this._offset,
                },
            }).then(function (entries) {
                var hasMore = entries.length > PAGE_SIZE;
                var page = entries.slice(0, PAGE_SIZE).map(self._decorate.bind(self));
                self._offset += page.length;
                self._appendEntries(page);
                self.$(".o_ai_trace_load_older").toggleClass("d-none", !hasMore);
                self._refreshEmpty();
            });
        },

        /**
         * Append entries to the day groups, merging with the last day.
         *
         * @private
         * @param {Array} entries decorated entries, newest first.
         */
        _appendEntries: function (entries) {
            var self = this;
            var groups = helpers.groupByDate(entries, function (entry) {
                return entry._day;
            });
            groups.forEach(function (group) {
                var $list = null;
                if (group.day === self._lastDay) {
                    $list = self.$(".o_ai_trace_day:last .o_ai_trace_list");
                } else {
                    var $day = $(
                        qweb.render("ssi_ai_trace_mixin.Day", {day: group.day})
                    );
                    self.$(".o_ai_trace_days").append($day);
                    $list = $day.find(".o_ai_trace_list");
                    self._lastDay = group.day;
                }
                group.entries.forEach(function (entry) {
                    $list.append(self._renderEntry(entry));
                });
            });
            this._hasEntries = this._hasEntries || entries.length > 0;
        },

        /**
         * Show the placeholder only when nothing at all was loaded.
         *
         * @private
         */
        _refreshEmpty: function () {
            this.$(".o_ai_trace_empty").toggleClass(
                "d-none",
                Boolean(this._hasSummaries || this._hasEntries)
            );
        },

        /**
         * Create one read-only Ace viewer on a DOM node.
         *
         * @private
         * @param {Node} node the target element.
         * @param {Object} spec ``mode`` and ``text`` from ``pickAceMode``.
         * @returns {Object} the Ace editor.
         */
        _createViewer: function (node, spec) {
            var editor = window.ace.edit(node);
            editor.setOptions({
                maxLines: 40,
                minLines: 1,
                showPrintMargin: false,
                readOnly: true,
                highlightActiveLine: false,
                highlightGutterLine: false,
            });
            editor.renderer.setOptions({
                displayIndentGuides: false,
                showGutter: false,
            });
            editor.renderer.$cursorLayer.element.style.display = "none";
            editor.$blockScrolling = true;
            var session = editor.getSession();
            session.setOptions({
                useWorker: false,
                mode: "ace/mode/" + spec.mode,
                tabSize: 2,
                useSoftTabs: true,
                wrap: true,
            });
            session.setValue(spec.text);
            return editor;
        },

        /**
         * Destroy the Ace viewers of one entry.
         *
         * @private
         * @param {String|Number} entryId the entry identifier.
         */
        _destroyViewers: function (entryId) {
            (this._viewers[entryId] || []).forEach(function (editor) {
                editor.destroy();
            });
            delete this._viewers[entryId];
        },

        /**
         * Fetch the long texts of an entry once.
         *
         * @private
         * @param {Number} entryId the entry identifier.
         * @returns {Promise} resolved with ``{prompt, action, result}``.
         */
        _fetchTexts: function (entryId) {
            var self = this;
            if (this._texts[entryId]) {
                return Promise.resolve(this._texts[entryId]);
            }
            return this._rpc({
                model: "ai_trace",
                method: "read",
                args: [[entryId], ["prompt", "action", "result"]],
            }).then(function (records) {
                self._texts[entryId] = records[0];
                return records[0];
            });
        },

        /**
         * Open an entry: load the libraries, then build the viewers.
         *
         * @private
         * @param {jQuery} $entry the entry element.
         * @returns {Promise}
         */
        _openEntry: function ($entry) {
            var self = this;
            var entryId = parseInt($entry.data("id"), 10);
            var libs = ajax.loadLibs({jsLibs: basic_fields.AceEditor.prototype.jsLibs});
            return Promise.all([this._fetchTexts(entryId), libs]).then(function (res) {
                if ($entry.find(".o_ai_trace_body").hasClass("d-none") === false) {
                    return;
                }
                var texts = res[0];
                var $body = $entry
                    .find(".o_ai_trace_body")
                    .empty()
                    .removeClass("d-none");
                $entry.find(".o_ai_trace_entry_header").attr("aria-expanded", "true");
                $entry.find(".o_ai_trace_snippet").addClass("d-none");
                self._viewers[entryId] = [];
                SECTIONS.forEach(function (section) {
                    if (!texts[section.name]) {
                        return;
                    }
                    var spec = helpers.pickAceMode(section.name, texts[section.name]);
                    var $section = $(
                        qweb.render("ssi_ai_trace_mixin.Section", {
                            title: section.title,
                        })
                    );
                    $body.append($section);
                    self._viewers[entryId].push(
                        self._createViewer($section.find(".o_ai_trace_ace")[0], spec)
                    );
                });
            });
        },

        /**
         * Close an entry and destroy its viewers.
         *
         * @private
         * @param {jQuery} $entry the entry element.
         */
        _closeEntry: function ($entry) {
            this._destroyViewers(parseInt($entry.data("id"), 10));
            $entry.find(".o_ai_trace_body").empty().addClass("d-none");
            $entry.find(".o_ai_trace_entry_header").attr("aria-expanded", "false");
            $entry.find(".o_ai_trace_snippet").removeClass("d-none");
        },

        // ----------------------------------------------------------------------
        // Handlers
        // ----------------------------------------------------------------------

        /**
         * @private
         * @param {MouseEvent} ev the click on an entry header.
         */
        _onToggleEntry: function (ev) {
            var $entry = $(ev.currentTarget).closest(".o_ai_trace_entry");
            if ($entry.find(".o_ai_trace_body").hasClass("d-none")) {
                this._openEntry($entry);
            } else {
                this._closeEntry($entry);
            }
        },

        /**
         * @private
         */
        _onLoadOlder: function () {
            this._loadPage();
        },
    });

    return Timeline;
});
