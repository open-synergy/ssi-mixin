// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_ai_trace_mixin.FormRenderer", function (require) {
    "use strict";

    // The include below overrides a method defined by the include of
    // ``mail``, so that one must be applied first.
    require("mail/static/src/widgets/form_renderer/form_renderer.js");

    var core = require("web.core");
    var FormRenderer = require("web.FormRenderer");
    var Timeline = require("ssi_ai_trace_mixin.Timeline");

    var qweb = core.qweb;

    FormRenderer.include({
        /**
         * @override
         */
        init: function () {
            this._super.apply(this, arguments);
            this._aiTraceTab = "chatter";
            this._aiTraceKey = undefined;
            this._aiTraceTimeline = undefined;
        },

        /**
         * @override
         */
        destroy: function () {
            this._destroyAiTraceTimeline();
            this._super.apply(this, arguments);
        },

        // ----------------------------------------------------------------------
        // Private
        // ----------------------------------------------------------------------

        /**
         * Tell whether the toggle must wrap the chatter of this form.
         *
         * Requires the hidden ``ai_trace_count`` marker field, a saved
         * record, and a form that is not shown in a dialog.
         *
         * @private
         * @returns {Boolean}
         */
        _hasAiTrace: function () {
            return Boolean(
                !this._isFromFormViewDialog &&
                    this.state &&
                    this.state.res_id &&
                    this.state.fields &&
                    this.state.fields.ai_trace_count
            );
        },

        /**
         * @private
         */
        _destroyAiTraceTimeline: function () {
            if (this._aiTraceTimeline) {
                this._aiTraceTimeline.destroy();
                this._aiTraceTimeline = undefined;
            }
        },

        /**
         * Keep the timeline alive across the re-render of the form.
         *
         * Emptying the form would drop the event handlers of the
         * timeline, so its element is detached first and put back by
         * ``_makeChatterContainerTarget``.
         *
         * @override
         */
        _renderView: function () {
            if (this._aiTraceTimeline) {
                this._aiTraceTimeline.$el.detach();
            }
            return this._super.apply(this, arguments);
        },

        /**
         * Wrap the chatter target with the Chatter | AI Trace toggle.
         *
         * @override
         */
        _makeChatterContainerTarget: function () {
            var $chatter = this._super.apply(this, arguments);
            if (!this._hasAiTrace()) {
                this._destroyAiTraceTimeline();
                this._aiTraceTab = "chatter";
                return $chatter;
            }
            var key = this.state.model + "," + this.state.res_id;
            if (this._aiTraceKey !== key) {
                // A different record (pager) always starts on Chatter.
                this._destroyAiTraceTimeline();
                this._aiTraceTab = "chatter";
                this._aiTraceKey = key;
            }
            var $wrapper = $('<div class="o_ai_trace_wrapper"/>');
            var $toggle = $(
                qweb.render("ssi_ai_trace_mixin.Toggle", {
                    tab: this._aiTraceTab,
                    count: this.state.data.ai_trace_count || 0,
                })
            );
            var $container = $('<div class="o_ai_trace_timeline_container"/>');
            $wrapper.append($toggle, $chatter, $container);
            if (this._aiTraceTimeline) {
                this._aiTraceTimeline.$el.appendTo($container);
            }
            this._applyAiTraceTab($wrapper);
            $toggle.on(
                "click",
                ".o_ai_trace_tab",
                this._onAiTraceTab.bind(this, $wrapper)
            );
            return $wrapper;
        },

        /**
         * Show the active tab and hide, never destroy, the other one.
         *
         * @private
         * @param {jQuery} $wrapper the toggle wrapper element.
         */
        _applyAiTraceTab: function ($wrapper) {
            var isTrace = this._aiTraceTab === "ai_trace";
            $wrapper
                .find(".o_FormRenderer_chatterContainer")
                .toggleClass("d-none", isTrace);
            $wrapper
                .find(".o_ai_trace_timeline_container")
                .toggleClass("d-none", !isTrace);
            $wrapper
                .find(".o_ai_trace_tab_chatter")
                .toggleClass("btn-primary", !isTrace)
                .toggleClass("btn-secondary", isTrace);
            $wrapper
                .find(".o_ai_trace_tab_trace")
                .toggleClass("btn-primary", isTrace)
                .toggleClass("btn-secondary", !isTrace);
        },

        /**
         * Create the timeline the first time the AI Trace tab is shown.
         *
         * @private
         * @param {jQuery} $wrapper the toggle wrapper element.
         */
        _ensureAiTraceTimeline: function ($wrapper) {
            if (this._aiTraceTimeline) {
                return;
            }
            this._aiTraceTimeline = new Timeline(this, {
                model: this.state.model,
                resId: this.state.res_id,
            });
            this._aiTraceTimeline.appendTo(
                $wrapper.find(".o_ai_trace_timeline_container")
            );
        },

        // ----------------------------------------------------------------------
        // Handlers
        // ----------------------------------------------------------------------

        /**
         * @private
         * @param {jQuery} $wrapper the toggle wrapper element.
         * @param {MouseEvent} ev the click on a toggle button.
         */
        _onAiTraceTab: function ($wrapper, ev) {
            this._aiTraceTab = $(ev.currentTarget).data("tab");
            if (this._aiTraceTab === "ai_trace") {
                this._ensureAiTraceTimeline($wrapper);
            }
            this._applyAiTraceTab($wrapper);
        },
    });
});
