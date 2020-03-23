# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.http import request
import logging
from odoo.addons.website_sale_delivery.controllers.main import WebsiteSaleDelivery

_logger = logging.getLogger(__name__)


class WebsiteSaleDeliveryNetwork(WebsiteSaleDelivery):

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        order = request.website.sale_get_order()
        carrier_id = post.get('carrier_id')
        from_location_id = int(post.get('from_location_id')) if post.get('from_location_id', False) else False
        to_location_id = post.get('to_location_id') if post.get('to_location_id', False) else False

        if carrier_id:
            carrier_id = int(carrier_id)
        if order:
            order._check_carrier_quotation(force_carrier_id=carrier_id)

            # 来源和目的地
            order._check_from_to_location(from_location_id=from_location_id, to_location_id=to_location_id)
            if carrier_id:
                return request.redirect("/shop/payment")

        return super(WebsiteSaleDelivery, self).payment(**post)

    def _update_website_sale_delivery(self, **post):
        order = request.website.sale_get_order()
        carrier_id = int(post['carrier_id'])
        from_location_id = int(post.get('from_location_id')) if post.get('from_location_id', False) else False
        to_location_id = int(post.get('to_location_id')) if post.get('to_location_id', False) else False

        if order:
            order._check_carrier_quotation(force_carrier_id=carrier_id)

            # 来源和目的地 填充
            order._check_from_to_location(from_location_id=from_location_id, to_location_id=to_location_id)

        return self._update_website_sale_delivery_return(order, **post)

    def _update_website_sale_delivery_return(self, order, **post):
        carrier_id = int(post.get('carrier_id'))
        from_location_id = int(post.get('from_location_id')) if post.get('from_location_id', False) else False
        to_location_id = int(post.get('to_location_id')) if post.get('to_location_id', False) else False

        currency = order.currency_id
        if order:
            new_amount_delivery = self._compute_new_amount_delivery_from_network(from_location_id, to_location_id)
            website_data = {
                'status': order.delivery_rating_success,
                'error_message': order.delivery_message,
                'carrier_id': carrier_id,
                'from_location_id': from_location_id,
                'to_location_id': to_location_id,
                'new_amount_delivery': self._format_amount(order.amount_delivery, currency),
                # 'new_amount_delivery': self._format_amount(new_amount_delivery, currency),
                'new_amount_untaxed': self._format_amount(order.amount_untaxed, currency),
                'new_amount_tax': self._format_amount(order.amount_tax, currency),
                'new_amount_total': self._format_amount(order.amount_total, currency),
            }
            return website_data
        return {}

    def _compute_new_amount_delivery_from_network(self, from_location_id, to_location_id):
        return 123

