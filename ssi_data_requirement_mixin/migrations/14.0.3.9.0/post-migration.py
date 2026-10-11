# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.3.8.0 -> 14.0.3.9.0
#
# Changes: Replace Many2many data_requirement_ids (per-model junction tables)
#          with One2many data_requirement_document_ids via data_requirement.document
#          (single generic link table).
#
# This script is intentionally a no-op at the mixin level.
# Each implementation module is responsible for migrating its own junction
# table rows into data_requirement_document.
# See ssi_helpdesk_data_requirement, ssi_lead_data_requirement, and
# ssi_odoo_implementation_data_requirement post-migration scripts.

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info(
        "ssi_data_requirement_mixin %s: data_requirement.document table "
        "will be created by Odoo ORM. Implementation modules handle data migration.",
        version,
    )
