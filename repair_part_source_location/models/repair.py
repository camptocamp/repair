# Copyright 2024 Camptocamp SA (https://www.camptocamp.com).
# @author: Italo Lopes <italo.lopes@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    parts_source_location_id = fields.Many2one(
        "stock.location",
        string="Repair part source location",
    )

    @api.onchange("picking_type_id")
    def _onchange_picking_type_id(self):
        if self.picking_type_id:
            self.parts_source_location_id = self.picking_type_id.default_location_src_id
