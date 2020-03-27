#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import werkzeug
import logging
import requests
from odoo.tools import config

_logger = logging.getLogger(__name__)


def urlplus(url, params):
    return werkzeug.Href(url)(params or None)


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


class ResPartner(models.Model):
    _inherit = 'res.partner'

    location_long = fields.Char('Longitude', compute='_compute_long_lat', store=True)
    location_lat = fields.Char('Latitude', compute='_compute_long_lat', store=True)

    @api.multi
    @api.depends('street')
    def _compute_long_lat(self):
        for line_id in self:
            if not line_id.street:
                continue
            lng_value, lat_value = get_long_lat_value(line_id.street)
            if not lng_value or not lat_value:
                continue
            _logger.info({
                'lng_value': lng_value,
                'lat_value': lat_value
            })
            line_id.location_long = lng_value
            line_id.location_lat = lat_value

    def baidu_map_img(self, zoom=15, width=298, height=298):
        country_name = self.country_id and self.country_id.name or ''
        state_name = self.state_id and self.state_id.name or ''
        city_name = self.city or ''
        street_name = self.street or ''
        street2_name = self.street2 or ''
        params = {
            'markers': '%s' % street2_name,
            'center': '%s%s%s%s' % (country_name, state_name, city_name, street_name),
            'height': "%s" % height,
            'width': "%s" % width,
            'zoom': zoom,
            'copyright': 1,
        }
        # http://lbsyun.baidu.com/index.php?title=static
        return urlplus('//api.map.baidu.com/staticimage', params)

    def baidu_map_link(self):
        partner_name = self.name
        city_name = self.city or ''
        street2_name = self.street2 or ''
        params = {
            'address': '%s,%s,%s' % (city_name, street2_name, partner_name),
            'output': 'html',
            'src': 'odoo',
        }
        # http://lbsyun.baidu.com/index.php?title=uri
        return urlplus('//api.map.baidu.com/geocoder', params)
