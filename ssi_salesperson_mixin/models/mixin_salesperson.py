# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MixinSalesperson(models.AbstractModel):
    """
    Abstract mixin that adds ``sale_team_id`` and ``salesperson_id`` fields
    with a computed ``allowed_salesperson_ids`` helper that limits the
    selectable salespersons to the members of the chosen sales team (or all
    internal users if no team is selected).

    An ``onchange_salesperson_id`` handler clears the salesperson whenever
    the sales team changes.
    """

    _name = "mixin.salesperson"
    _description = "Salesperson Mixin"

    sale_team_id = fields.Many2one(
        comodel_name="crm.team",
    )

    @api.depends(
        "sale_team_id",
    )
    def _compute_allowed_salesperson_ids(self):
        """Compute the salespersons selectable for each record.

        Members of the chosen sales team, or all active internal users
        (including implied membership) when no team is chosen.
        """
        internal_user = self.env.ref("base.group_user")
        all_internal_users = self.env["res.users"].search(
            [("all_group_ids", "in", internal_user.ids)]
        )
        for record in self:
            result = all_internal_users.ids
            if record.sale_team_id:
                result = record.sale_team_id.member_ids.ids
            record.allowed_salesperson_ids = result

    allowed_salesperson_ids = fields.Many2many(
        comodel_name="res.users",
        compute="_compute_allowed_salesperson_ids",
        store=False,
    )

    salesperson_id = fields.Many2one(
        comodel_name="res.users",
    )

    @api.onchange(
        "sale_team_id",
    )
    def onchange_salesperson_id(self):
        self.salesperson_id = False
