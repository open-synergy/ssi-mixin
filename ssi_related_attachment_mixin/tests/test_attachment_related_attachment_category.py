# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAttachmentRelatedAttachmentCategory(YamlTransactionCase):
    def test_attachment_related_attachment_category(self):
        self.run_yaml_scenario("test_data_attachment_related_attachment_category.yaml")
