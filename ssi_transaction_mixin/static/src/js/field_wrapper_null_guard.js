// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_transaction_mixin.FieldWrapperNullGuard", function (require) {
    "use strict";

    var FieldWrapper = require("web.FieldWrapper");
    var utils = require("web.utils");

    // Odoo 14.0 wraps the ``boolean`` and ``badge`` field widgets in
    // ``FieldWrapper``. Most of its public methods dereference
    // ``this.componentRef.comp`` without checking that the wrapped OWL
    // component is mounted, which throws a TypeError when a renderer pass
    // races the mount (or the unmount). Only ``isSet()`` has such a guard
    // in core. Each guard below calls ``_super`` untouched when the
    // component exists and returns a safe value when it is null. The
    // per-instance property getters defined in the constructor are out of
    // scope: they are non-configurable own properties, which
    // ``utils.patch`` cannot reach.
    utils.patch(FieldWrapper, "ssi_transaction_mixin.FieldWrapperNullGuard", {
        /**
         * @override
         */
        mounted: function () {
            if (this.componentRef.comp) {
                return this._super.apply(this, arguments);
            }
            // Skip only the ``__node`` write; keep the parent behavior.
            var parent = Object.getPrototypeOf(FieldWrapper.prototype);
            if (parent && typeof parent.mounted === "function") {
                return parent.mounted.apply(this, arguments);
            }
        },

        /**
         * @override
         */
        activate: function () {
            if (this.componentRef.comp) {
                return this._super.apply(this, arguments);
            }
            return false;
        },

        /**
         * @override
         */
        commitChanges: function () {
            if (this.componentRef.comp) {
                return this._super.apply(this, arguments);
            }
            return Promise.resolve();
        },

        /**
         * @override
         */
        getFocusableElement: function () {
            if (this.componentRef.comp) {
                return this._super.apply(this, arguments);
            }
            return $();
        },

        /**
         * @override
         */
        isEmpty: function () {
            if (this.componentRef.comp) {
                return this._super.apply(this, arguments);
            }
            return !this.isSet();
        },

        /**
         * @override
         */
        isFocusable: function () {
            if (this.componentRef.comp) {
                return this._super.apply(this, arguments);
            }
            return false;
        },

        /**
         * @override
         */
        isValid: function () {
            if (this.componentRef.comp) {
                return this._super.apply(this, arguments);
            }
            return true;
        },

        /**
         * @override
         */
        removeInvalidClass: function () {
            if (this.componentRef.comp) {
                return this._super.apply(this, arguments);
            }
        },

        /**
         * @override
         */
        setIDForLabel: function () {
            if (this.componentRef.comp) {
                return this._super.apply(this, arguments);
            }
        },

        /**
         * @override
         */
        setInvalidClass: function () {
            if (this.componentRef.comp) {
                return this._super.apply(this, arguments);
            }
        },

        /**
         * The modifiers are still written to the shared props object, so
         * a component mounted later receives them anyway.
         *
         * @override
         */
        updateModifiersValue: function (modifiers) {
            if (this.componentRef.comp) {
                return this._super.apply(this, arguments);
            }
            if (this.props.options.attrs) {
                this.props.options.attrs.modifiersValue = modifiers || {};
            } else {
                var viewType = this.props.options.viewType || "default";
                var fieldsInfo = this.props.record.fieldsInfo[viewType];
                fieldsInfo[this.props.fieldName].modifiersValue = modifiers || {};
            }
        },
    });
});
