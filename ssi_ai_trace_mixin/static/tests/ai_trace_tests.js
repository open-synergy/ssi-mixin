odoo.define("ssi_ai_trace_mixin.ai_trace_tests", function (require) {
    "use strict";
    /* global QUnit*/

    var helpers = require("ssi_ai_trace_mixin.helpers");

    QUnit.module("ssi_ai_trace_mixin", {}, function () {
        QUnit.test("prompt and result use the markdown mode", function (assert) {
            assert.expect(3);
            assert.deepEqual(helpers.pickAceMode("prompt", "# Hi"), {
                mode: "markdown",
                text: "# Hi",
            });
            assert.deepEqual(helpers.pickAceMode("result", "ok"), {
                mode: "markdown",
                text: "ok",
            });
            assert.deepEqual(helpers.pickAceMode("prompt", null), {
                mode: "markdown",
                text: "",
            });
        });

        QUnit.test("a valid JSON action is pretty-printed in json mode", function (
            assert
        ) {
            assert.expect(2);
            var spec = helpers.pickAceMode("action", '{"a":1,"b":[2]}');
            assert.strictEqual(spec.mode, "json");
            assert.strictEqual(spec.text, JSON.stringify({a: 1, b: [2]}, null, 2));
        });

        QUnit.test("an action that is not JSON falls back to text", function (assert) {
            assert.expect(3);
            assert.deepEqual(helpers.pickAceMode("action", "not { json"), {
                mode: "text",
                text: "not { json",
            });
            assert.strictEqual(helpers.pickAceMode("action", "").mode, "text");
            assert.strictEqual(helpers.pickAceMode("action", null).mode, "text");
        });

        QUnit.test("entries are grouped by consecutive day", function (assert) {
            assert.expect(4);
            var entries = [
                {id: 1, day: "d2"},
                {id: 2, day: "d2"},
                {id: 3, day: "d1"},
            ];
            var groups = helpers.groupByDate(entries, function (entry) {
                return entry.day;
            });
            assert.strictEqual(groups.length, 2);
            assert.strictEqual(groups[0].day, "d2");
            assert.deepEqual(
                groups[0].entries.map(function (entry) {
                    return entry.id;
                }),
                [1, 2]
            );
            assert.deepEqual(
                helpers.groupByDate([], function () {
                    return "x";
                }),
                []
            );
        });

        QUnit.test("the snippet is one plain line of at most 160 characters", function (
            assert
        ) {
            assert.expect(3);
            assert.strictEqual(helpers.makeSnippet("a\n\n b\t c"), "a b c");
            assert.strictEqual(helpers.makeSnippet(null), "");
            assert.strictEqual(
                helpers.makeSnippet(new Array(400).join("x")).length,
                160
            );
        });
    });
});
