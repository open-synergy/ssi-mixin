Inherit ``mixin.ai_trace`` in the model that must carry traces, for example
``_inherit = ["mixin.ai_trace"]``. Every form view of that model which contains
the chatter then gets the ``Chatter | AI Trace (n)`` toggle without editing the
view.

Give the account that writes the entries the ``AI Trace Writer`` group, then
call the API with a list of entries::

    env["ai_trace"].ai_trace_append([{
        "model": "res.partner",
        "res_id": 7,
        "session_key": "session-1",
        "turn": 1,
        "kind": "turn",
        "prompt": "...",
        "action": "{}",
        "result": "...",
    }])

The retention period in days is the system parameter
``ssi_ai_trace_mixin.retention_days`` (default ``180``, ``0`` keeps everything).
Summary entries are never purged.
