#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    location_long = fields.Char('Longitude', related='partner_id.location_long')
    location_lat = fields.Char('Latitude', related='partner_id.location_lat')
    service_area = fields.Float('Service area')

    location_name = fields.Char('Location')
