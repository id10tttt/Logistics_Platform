#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    from_warehouse_id = fields.Many2one('stock.warehouse', string='From')
    to_warehouse_id = fields.Many2one('stock.warehouse', string='To')

    def _check_from_to_warehouse(self, from_warehouse_id=None, to_warehouse_id=None):
        try:
            self.write({
                'from_warehouse_id': from_warehouse_id,
                'to_warehouse_id': to_warehouse_id
            })
        except Exception as e:
            pass
