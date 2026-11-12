// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_transaction_mixin.FieldWrapperNullGuard", function (require) {
    "use strict";

    var FieldWrapper = require("web.FieldWrapper");
    var utils = require("web.utils");

    // Odoo 14.0 wraps the ``boolean`` and ``badge`` field widgets in
    // ``FieldWrapper``. Its ``updateModifiersValue`` re-assigns the props
    // of the wrapped OWL component without checking that the component is
    // mounted yet, which throws a TypeError when a modifiers pass races
    // the mount. The guard below mirrors the one core already has in
    // ``isSet()``: the modifiers are still written to the shared props
    // object, so a component mounted later receives them anyway.
    utils.patch(FieldWrapper, "ssi_transaction_mixin.FieldWrapperNullGuard", {
        /**
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
