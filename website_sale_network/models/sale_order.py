#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    from_location_id = fields.Many2one('stock.location', string='From')
    to_location_id = fields.Many2one('stock.location', string='To')

    def _check_from_to_location(self, from_location_id=None, to_location_id=None):
        try:
            self.write({
                'from_location_id': from_location_id,
                'to_location_id': to_location_id
            })
        except Exception as e:
            pass
