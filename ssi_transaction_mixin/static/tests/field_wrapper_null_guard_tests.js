// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_transaction_mixin.field_wrapper_null_guard_tests", function (require) {
    "use strict";
    /* global QUnit*/

    var FieldWrapper = require("web.FieldWrapper");
    require("ssi_transaction_mixin.FieldWrapperNullGuard");

    /**
     * Build a fake wrapper carrying only what updateModifiersValue reads.
     *
     * @param {Object} comp the mounted component, or null
     * @param {Object} options the props options
     * @returns {Object}
     */
    function makeWrapper(comp, options) {
        var fieldsInfo = {default: {flag: {}}};
        return {
            componentRef: {comp: comp},
            props: {
                options: options,
                fieldName: "flag",
                record: {fieldsInfo: fieldsInfo},
            },
        };
    }

    function callUpdate(wrapper, modifiers) {
        return FieldWrapper.prototype.updateModifiersValue.call(wrapper, modifiers);
    }

    QUnit.module("ssi_transaction_mixin", {}, function () {
        QUnit.test("unmounted component with attrs does not throw", function (assert) {
            assert.expect(2);
            var attrs = {};
            var wrapper = makeWrapper(null, {attrs: attrs});
            callUpdate(wrapper, {invisible: true});
            assert.deepEqual(attrs.modifiersValue, {invisible: true});
            assert.strictEqual(wrapper.componentRef.comp, null);
        });

        QUnit.test("unmounted component without attrs uses fieldsInfo", function (
            assert
        ) {
            assert.expect(1);
            var wrapper = makeWrapper(null, {});
            callUpdate(wrapper, {readonly: true});
            assert.deepEqual(
                wrapper.props.record.fieldsInfo.default.flag.modifiersValue,
                {
                    readonly: true,
                }
            );
        });

        QUnit.test("mounted component keeps the core behavior", function (assert) {
            assert.expect(2);
            var comp = {props: null};
            var attrs = {};
            var wrapper = makeWrapper(comp, {attrs: attrs});
            callUpdate(wrapper, {invisible: false});
            assert.strictEqual(comp.props, wrapper.props);
            assert.deepEqual(attrs.modifiersValue, {invisible: false});
        });

        QUnit.test("undefined modifiers become an empty object", function (assert) {
            assert.expect(1);
            var attrs = {};
            var wrapper = makeWrapper(null, {attrs: attrs});
            callUpdate(wrapper, undefined);
            assert.deepEqual(attrs.modifiersValue, {});
        });
    });
});
