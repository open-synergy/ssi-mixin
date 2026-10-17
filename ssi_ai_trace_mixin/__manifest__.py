# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "AI Trace Mixin",
    "version": "14.0.1.0.0",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "base",
        "web",
        "mail",
        "ssi_web_widget_ace_mode",
    ],
    "data": [
        "security/res_groups/ai_trace.xml",
        "security/ir_model_access/ai_trace.xml",
        "security/ir_rule/ai_trace.xml",
        "data/ir_config_parameter_data.xml",
        "data/ir_cron_data.xml",
        "menu.xml",
        "views/ai_trace.xml",
        "views/assets.xml",
    ],
    "qweb": [
        "static/src/xml/ai_trace_timeline.xml",
    ],
}
