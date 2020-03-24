# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.http import request
import logging
import requests
from odoo.tools import config
from math import *
from odoo.addons.website_sale_delivery.controllers.main import WebsiteSaleDelivery

_logger = logging.getLogger(__name__)


class WebsiteSaleDeliveryNetwork(WebsiteSaleDelivery):

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        order = request.website.sale_get_order()
        carrier_id = post.get('carrier_id')
        from_location_name = post.get('from_location_name') if post.get('from_location_name', False) else False
        to_location_name = post.get('to_location_name') if post.get('to_location_name', False) else False

        from_location_id, to_location_id = self.find_correct_belong_position(from_location_name, to_location_name)

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
        from_location_name = post.get('from_location_name') if post.get('from_location_name', False) else False
        to_location_name = post.get('to_location_name') if post.get('to_location_name', False) else False

        _logger.info({
            'from_location_name': from_location_name,
            'to_location_name': to_location_name
        })
        from_location_id, to_location_id = self.find_correct_belong_position(from_location_name, to_location_name)

        if order:
            order._check_carrier_quotation(force_carrier_id=carrier_id)

            # 来源和目的地 填充
            order._check_from_to_location(from_location_id=from_location_id, to_location_id=to_location_id)

        return self._update_website_sale_delivery_return(order, **post)

    def _update_website_sale_delivery_return(self, order, **post):
        carrier_id = int(post.get('carrier_id'))

        from_location_name = post.get('from_location_name') if post.get('from_location_name', False) else False
        to_location_name = post.get('to_location_name') if post.get('to_location_name', False) else False

        from_location_id, to_location_id = self.find_correct_belong_position(from_location_name, to_location_name)

        currency = order.currency_id
        if order:
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

    def find_correct_belong_position(self, from_location_name, to_location_name):
        from_long, from_lat = self.get_lat_long_value(from_location_name)
        to_long, to_lat = self.get_lat_long_value(to_location_name)

        from_location_id = self.find_close_service_area(from_long, from_lat)
        to_location_id = self.find_close_service_area(to_long, to_lat)
        return 1, 2

    def find_close_service_area(self, from_long, from_lat):
        location_ids = self.env['stock.location'].search([])

        for location_id in location_ids:
            distance_value = self.get_distance(from_long, from_lat, location_id.location_long, location_id.location_lat)
            if distance_value < location_id.service_area:
                return location_id
        return False

    # 获取经纬度
    def get_long_lat_value(self, name):
        if not name:
            return
        url = 'https://restapi.amap.com/v3/geocode/geo?parameters'
        parameters = {
            'address': name,
            'key': '30a60cbd0f9e2825703208a9decff925'
        }
        _logger.info({
            'parameters': parameters
        })
        res = requests.get(url=url, params=parameters)
        if res.status_code == 200:
            geocodes_value = res.json().get('geocodes')
            location_info = geocodes_value.get('location')
            long_value, lat_value = location_info.split(',')
            return long_value, lat_value

    def get_distance(self, longitude_1, latitude_1, longitude_2, latitude_2):
        """"

        计算两个经纬度点之间的直线距离
        :param longitude_1: 第1个点经度
        :param latitude_1: 第1个点维度
        :param longitude_2: 第2个点经度
        :param latitude_2: 第2个点维度
        :return: 距离 km
        """
        # 经纬度转换成弧度
        # lng1,lat1,lng2,lat2 = (120.12802999999997,30.28708,115.86572000000001,28.7427)　
        lng1, lat1, lng2, lat2 = map(radians, [float(longitude_1) / 1000000, float(latitude_1) / 1000000,
                                               float(longitude_2) / 1000000, float(latitude_2) / 1000000])
        d_lon = lng2 - lng1
        d_lat = lat2 - lat1
        a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
        distance = 2 * asin(sqrt(a)) * 6371 * 1000  # 地球平均半径，6371km
        distance = round(distance / 1000, 3)

        return distance
