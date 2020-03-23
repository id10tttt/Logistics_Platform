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
        return {
            'success': True,
            'price': 0.0,
            'error_message': False,
            'warning_message': False
        }
