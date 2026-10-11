from odoo import models


class SchemaParserCategory(models.Model):
    """
    Master-data model (inheriting ``mixin.master_data``) that categorises
    ``schema_parser`` records into logical groups.
    """

    _name = "schema_parser_category"
    _description = "Schema Parser Category"
    _inherit = "mixin.master_data"
