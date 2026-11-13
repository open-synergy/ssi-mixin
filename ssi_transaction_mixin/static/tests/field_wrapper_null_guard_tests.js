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

    /**
     * Call a patched prototype method on a fake wrapper.
     *
     * @param {String} name the method name
     * @param {Object} wrapper the fake wrapper
     * @param {Array} args the call arguments
     * @returns {*}
     */
    function callMethod(name, wrapper, args) {
        return FieldWrapper.prototype[name].apply(wrapper, args || []);
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

        QUnit.test("null component returns safe values", function (assert) {
            assert.expect(6);
            var wrapper = makeWrapper(null, {});
            wrapper.isSet = function () {
                return false;
            };
            assert.strictEqual(callMethod("isEmpty", wrapper), true, "isEmpty");
            assert.strictEqual(callMethod("isValid", wrapper), true, "isValid");
            assert.strictEqual(
                callMethod("isFocusable", wrapper),
                false,
                "isFocusable"
            );
            assert.strictEqual(callMethod("activate", wrapper), false, "activate");
            assert.strictEqual(
                callMethod("getFocusableElement", wrapper).length,
                0,
                "getFocusableElement"
            );
            assert.strictEqual(
                callMethod("mounted", wrapper),
                undefined,
                "mounted does not throw"
            );
        });

        QUnit.test("null component isEmpty follows isSet", function (assert) {
            assert.expect(1);
            var wrapper = makeWrapper(null, {});
            wrapper.isSet = function () {
                return true;
            };
            assert.strictEqual(callMethod("isEmpty", wrapper), false);
        });

        QUnit.test("null component class helpers are no-ops", function (assert) {
            assert.expect(3);
            var wrapper = makeWrapper(null, {});
            assert.strictEqual(callMethod("removeInvalidClass", wrapper), undefined);
            assert.strictEqual(callMethod("setInvalidClass", wrapper), undefined);
            assert.strictEqual(callMethod("setIDForLabel", wrapper, ["x"]), undefined);
        });

        QUnit.test("null component commitChanges resolves", function (assert) {
            assert.expect(1);
            var done = assert.async();
            var wrapper = makeWrapper(null, {});
            callMethod("commitChanges", wrapper).then(function (res) {
                assert.strictEqual(res, undefined);
                done();
            });
        });

        QUnit.test("mounted component delegates to core", function (assert) {
            assert.expect(6);
            var calls = [];
            var comp = {
                isEmpty: "E",
                isValid: "V",
                isFocusable: "F",
                focusableElement: null,
                activate: function () {
                    calls.push("activate");
                    return "A";
                },
                commitChanges: function () {
                    calls.push("commit");
                    return "C";
                },
                removeInvalidClass: function () {
                    calls.push("rm");
                },
                setInvalidClass: function () {
                    calls.push("set");
                },
                setIdForLabel: function () {
                    calls.push("id");
                },
            };
            var wrapper = makeWrapper(comp, {});
            assert.strictEqual(callMethod("isEmpty", wrapper), "E");
            assert.strictEqual(callMethod("isValid", wrapper), "V");
            assert.strictEqual(callMethod("isFocusable", wrapper), "F");
            assert.strictEqual(callMethod("activate", wrapper), "A");
            assert.strictEqual(callMethod("commitChanges", wrapper), "C");
            callMethod("removeInvalidClass", wrapper);
            callMethod("setInvalidClass", wrapper);
            callMethod("setIDForLabel", wrapper);
            assert.deepEqual(calls, ["activate", "commit", "rm", "set", "id"]);
        });

        QUnit.test("errors of a mounted component still propagate", function (assert) {
            assert.expect(1);
            var wrapper = makeWrapper(
                {
                    commitChanges: function () {
                        throw new Error("boom");
                    },
                },
                {}
            );
            assert.throws(function () {
                callMethod("commitChanges", wrapper);
            }, /boom/);
        });
    });
});
