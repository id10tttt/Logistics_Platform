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
            order._check_from_to_warehouse(from_warehouse_id=from_location_id, to_warehouse_id=to_location_id)
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
            order._check_from_to_warehouse(from_warehouse_id=from_location_id, to_warehouse_id=to_location_id)

        return self._update_website_sale_delivery_return(order, **post)

    def _update_website_sale_delivery_return(self, order, **post):
        carrier_id = int(post.get('carrier_id'))

        from_location_name = post.get('from_location_name') if post.get('from_location_name', False) else False
        to_location_name = post.get('to_location_name') if post.get('to_location_name', False) else False

        _logger.info({
            'from_location_name': from_location_name,
            'to_location_name': to_location_name
        })
        from_warehouse_id, to_warehouse_id = self.find_correct_belong_position(from_location_name, to_location_name)

        currency = order.currency_id
        if order:
            website_data = {
                'status': order.delivery_rating_success,
                'error_message': order.delivery_message,
                'carrier_id': carrier_id,
                'from_warehouse_id': from_warehouse_id.id,
                'to_warehouse_id': to_warehouse_id.id,
                'new_amount_delivery': self._format_amount(order.amount_delivery, currency),
                # 'new_amount_delivery': self._format_amount(new_amount_delivery, currency),
                'new_amount_untaxed': self._format_amount(order.amount_untaxed, currency),
                'new_amount_tax': self._format_amount(order.amount_tax, currency),
                'new_amount_total': self._format_amount(order.amount_total, currency),
            }
            return website_data
        return {}

    def find_correct_belong_position(self, from_location_name, to_location_name):
        if not from_location_name or not to_location_name:
            return False, False

        from_long, from_lat = self.get_long_lat_value(from_location_name)
        to_long, to_lat = self.get_long_lat_value(to_location_name)

        _logger.info({
            'from_long': from_long,
            'from_lat': from_lat,
            'to_long': to_long,
            'to_lat': to_lat
        })
        from_warehouse_id = self.find_close_service_area(from_long, from_lat)
        to_warehouse_id = self.find_close_service_area(to_long, to_lat)
        _logger.info({
            'from_warehouse_id': from_warehouse_id,
            'to_warehouse_id': to_warehouse_id
        })
        if from_warehouse_id and to_warehouse_id:
            return from_warehouse_id, to_warehouse_id
        return 1, 1

    def find_close_service_area(self, from_long, from_lat):
        warehouse_ids = request.env['stock.warehouse'].sudo().search([])

        for warehouse_id in warehouse_ids:
            # distance_value = self.get_distance(from_long, from_lat, warehouse_id.location_long,
            #                                    warehouse_id.location_lat)
            distance_value = self.get_distance_by_gaode(from_long + ',' + from_lat,
                                                        warehouse_id.location_long + ',' + warehouse_id.location_lat)
            if distance_value < warehouse_id.service_area:
                return warehouse_id
        return False

    # 获取经纬度
    def get_long_lat_value(self, name):
        if not name:
            return
        url = 'https://restapi.amap.com/v3/geocode/geo?parameters'
        parameters = {
            'address': name,
            'key': config.get('gaode_map_web_service_key')
        }
        res = requests.get(url=url, params=parameters)
        if res.status_code == 200:
            geocodes_value = res.json().get('geocodes')
            if geocodes_value:
                geocodes_value = geocodes_value[0]
            else:
                return False, False
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

    def get_distance_by_gaode(self, origins, destination):
        parameters = {
            'origins': origins,
            'destination': destination,
            'key': config.get('gaode_map_web_service_key'),
            'type': 0
        }
        url = 'https://restapi.amap.com/v3/distance?parameters'
        res = requests.get(url=url, params=parameters)
        if res.status_code == 200:
            distance_res = res.json().get('results')[0]
            # _logger.info({
            #     'distance_res': distance_res
            # })
            # 高德返回米， 转换成公里
            return float(distance_res.get('distance')) / 1000
        return 0
