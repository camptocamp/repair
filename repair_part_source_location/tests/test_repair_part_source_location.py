# Copyright 2024 Camptocamp SA (https://www.camptocamp.com).
# @author: Italo Lopes <italo.lopes@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tests.common import TransactionCase


class TestRepairPartSourceLocation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.part_location_test = cls.env["stock.location"].create(
            {
                "name": "Test Part Location",
                "usage": "internal",
                "location_id": cls.env.ref("stock.stock_location_stock").id,
            }
        )
        cls.product_to_repair = cls.env.ref("product.product_product_4")
        cls.product_part = cls.env["product.product"].create(
            {
                "name": "Part To Use",
                "type": "product",
            }
        )
        cls.env["stock.quant"].create(
            {
                "product_id": cls.product_part.id,
                "location_id": cls.part_location_test.id,
                "quantity": 10,
            }
        )

        cls.picking_type_id = cls.env.ref("repair.picking_type_warehouse0_repair")
        cls.repair_order = cls.env["repair.order"].create(
            {
                "name": "Test Repair Order",
                "product_id": cls.product_to_repair.id,
                "picking_type_id": cls.picking_type_id.id,
                "parts_source_location_id": cls.part_location_test.id,
            }
        )

        cls.default_location_src_id = cls.picking_type_id.default_location_src_id
        cls.default_location_dest_id = cls.picking_type_id.default_location_dest_id
        cls.default_remove_location_dest_id = (
            cls.picking_type_id.default_remove_location_dest_id
        )
        cls.default_recycle_location_dest_id = (
            cls.picking_type_id.default_recycle_location_dest_id
        )

    def _create_move_line(self, repair_line_type):
        self.repair_order.write(
            {
                "move_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Add Component",
                            "repair_line_type": repair_line_type,
                            "product_id": self.product_part.id,
                            "product_uom_qty": 3,
                        },
                    )
                ]
            }
        )

    def _run_repair_actions(self):
        self.repair_order.action_validate()
        self.repair_order.action_repair_start()
        self.repair_order.action_repair_end()

    def test_01_repair_part_source_location(self):
        self._create_move_line("add")

        self._run_repair_actions()

        move_line_ids = self.env["stock.move.line"].search(
            [("move_id.repair_id", "=", self.repair_order.id)]
        )

        move_part_line_to_check = move_line_ids.filtered(
            lambda x: x.product_id == self.product_part
        )
        self.assertEqual(move_part_line_to_check.location_id, self.part_location_test)
        self.assertEqual(
            move_part_line_to_check.location_dest_id, self.default_location_dest_id
        )

        move_product_line_to_check = move_line_ids.filtered(
            lambda x: x.product_id == self.product_to_repair
        )
        self.assertEqual(
            move_product_line_to_check.location_id, self.default_location_src_id
        )
        self.assertEqual(
            move_product_line_to_check.location_dest_id, self.default_location_src_id
        )

    def test_02_repair_part_source_location_no_changes(self):
        self._create_move_line("remove")

        self._run_repair_actions()

        move_line_ids = self.env["stock.move.line"].search(
            [("move_id.repair_id", "=", self.repair_order.id)]
        )

        move_part_line_to_check = move_line_ids.filtered(
            lambda x: x.product_id == self.product_part
        )
        self.assertEqual(
            move_part_line_to_check.location_id, self.default_location_dest_id
        )
        self.assertEqual(
            move_part_line_to_check.location_dest_id,
            self.default_remove_location_dest_id,
        )
