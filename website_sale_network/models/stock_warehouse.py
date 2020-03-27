#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import logging
from odoo.tools import config

_logger = logging.getLogger(__name__)


# 获取经纬度
def get_long_lat_value(name):
    if not name:
        return
    url = 'https://restapi.amap.com/v3/geocode/geo?parameters'
    parameters = {
        'address': name,
        'key': config.get('gaode_map_web_service_key')
    }
    _logger.info({
        'parameters': parameters
    })
    res = requests.get(url=url, params=parameters)
    if res.status_code == 200:
        geocodes_value = res.json().get('geocodes')[0] if res.json().get('geocodes', False) else False
        if not geocodes_value:
            return False, False
        location_info = geocodes_value.get('location')
        long_value, lat_value = location_info.split(',')
        return long_value, lat_value
    else:
        return False, False


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    location_long = fields.Char('Longitude', related='partner_id.location_long', store=True, readonly=True)
    location_lat = fields.Char('Latitude', related='partner_id.location_lat', store=True, readonly=True)
    service_area = fields.Float('Service area')

    location_name = fields.Char('Location', related='partner_id.street', store=True, readonly=True)

    # @api.multi
    # @api.depends('location_name')
    # def _compute_location_lng_lat(self):
    #     for line_id in self:
    #         if not line_id.location_name:
    #             continue
    #
    #         lng_value, lat_value = get_long_lat_value(line_id.location_name)
    #         if not lng_value or not lat_value:
    #             continue
    #         _logger.info({
    #             'lng_value': lng_value,
    #             'lat_value': lat_value
    #         })
    #         line_id.location_long = lng_value
    #         line_id.location_lat = lat_value


