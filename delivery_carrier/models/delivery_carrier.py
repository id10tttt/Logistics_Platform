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

    # TODO: 调用网络里面的计算方法，获取价格参数，计算价格
    def get_price_from_netwrok_by_location(self, from_location_id, to_location_id):
        if not from_location_id or not to_location_id:
            return 0.0
        else:
            route_network_obj = self.env['route.network']
            network_ids = route_network_obj.sudo().search([])

            return_values = []
            for network_id in network_ids:
                network_id.generate_all_delivery_network()
                network_id.find_out_shortest_path_with_networkx(from_location_id=from_location_id,
                                                                to_location_id=to_location_id)

                shortest_weight = network_id.shortest_weight

                if shortest_weight > 0:
                    return_values.append(shortest_weight)

            if return_values:
                return sorted(return_values)[0]
            else:
                return 0.0
