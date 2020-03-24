#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockLocation(models.Model):
    _inherit = 'stock.location'

    location_long = fields.Char('Longitude')
    location_lat = fields.Char('Latitude')
    service_area = fields.Float('Service area')
