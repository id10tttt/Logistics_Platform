#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
import logging

_logger = logging.getLogger(__name__)


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    delivery_type = fields.Selection(selection_add=[('network', "Network")])
    network_id = fields.Many2one('route.network', 'Network')

    # 网络计算方式的价格
    def network_rate_shipment(self, order):
        _logger.info({
            'from_location_id': order.from_location_id,
            'to_location_id': order.to_location_id
        })
        price_total = self.get_price_from_netwrok_by_location(order.from_location_id, order.to_location_id)
        return {
            'success': True,
            'price': price_total,
            'error_message': False,
            'warning_message': False
        }

    def get_price_from_netwrok_by_location(self, from_location_id, to_location_id):
        if not from_location_id or not to_location_id:
            return 0.0
        else:
            return 99.9

