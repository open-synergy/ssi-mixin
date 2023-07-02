# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class MixinAccountMove(models.AbstractModel):
    _name = "mixin.account_move"
    _description = "Accounting Entry Header Mixin"
    _journal_id_field_name = "journal_id"
    _move_id_field_name = "move_id"
    _accounting_date_field_name = "data"
    _currency_id_field_name = "currency_id"
    _company_currency_id_field_name = "company_currency_id"

    def _create_standard_move(self):
        self.ensure_one()
        Move = self.env["account.move"]
        move = Move.with_context(check_move_validity=False).create(
            self._prepare_standard_move()
        )
        self.write(
            {
                self._move_id_field_name: move.id,
            }
        )

    def _post_standard_move(self):
        self.ensure_one()
        move = getattr(self, self._move_id_field_name)
        move.action_post()

    def _prepare_standard_move(self):
        self.ensure_one()
        return {
            "name": self.name,
            "journal_id": getattr(self, self._journal_id_field_name).id,
            "date": getattr(self, self._accounting_date_field_name),
        }

    def _delete_standard_move(self):
        self.ensure_one()
        Move = self.env["account.move"]
        move = Move.with_context(check_move_validity=False).create(
            self._prepare_standard_move()
        )
        self.write(
            {
                self._move_id_field_name: move.id,
            }
        )

        move = getattr(self, self._move_id_field_name)

        if not move:
            return True

        self.write(
            {
                self._move_id_field_name: False,
            }
        )

        move.unlink()
