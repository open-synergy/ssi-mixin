# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MixinDataRequirementConfigurator(models.AbstractModel):
    """
    Abstract mixin that adds a ``data_requirement_ids`` One2many to any model,
    allowing the configuration of which data requirement packages are
    applicable to records of that model.

    Typically applied to type/category master-data models that configure
    which data is required when creating transactional records of a specific
    type.
    """

    _name = "mixin.data_requirement_configurator"
    _description = "Data Requirement Configurator Mixin"

    data_requirement_ids = fields.One2many(
        string="Data Requirements",
        comodel_name="data_requirement_configurator",
        inverse_name="object_id",
        domain=lambda self: [("model_name", "=", self._name)],
        auto_join=True,
    )

    def unlink(self):
        for record in self.sudo():
            record.data_requirement_ids.unlink()
        _super = super(MixinDataRequirementConfigurator, self)
        _super.unlink()
