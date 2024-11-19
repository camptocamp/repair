# Copyright 2024 Camptocamp SA (https://www.camptocamp.com).
# @author: Italo Lopes <italo.lopes@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models

from odoo.addons.repair.models.stock_move import (
    MAP_REPAIR_LINE_TYPE_TO_MOVE_LOCATIONS_FROM_REPAIR,
)

MAP_REPAIR_LINE_TYPE_TO_MOVE_LOCATIONS_FROM_REPAIR["add"] = {
    "location_id": "parts_source_location_id",
    "location_dest_id": "location_dest_id",
}


class StockMove(models.Model):
    _inherit = "stock.move"
