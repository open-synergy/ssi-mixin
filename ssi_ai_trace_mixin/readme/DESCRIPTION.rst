Stores the notes an AI assistant writes against any document in a dedicated
``ai_trace`` model instead of the chatter, so that a high volume of entries
neither bloats ``mail_message`` nor notifies followers or portal users.

Entries are written through the idempotent ``ai_trace_append`` API, purged by a
daily cron after a configurable retention period, and shown on the form view
in the chatter position through a ``Chatter | AI Trace (n)`` toggle.
