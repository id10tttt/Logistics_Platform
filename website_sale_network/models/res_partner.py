#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    location_long = fields.Char('Longitude', compute='_compute_long_lat', store=True)
    location_lat = fields.Char('Latitude', compute='_compute_long_lat', store=True)

    def _compute_long_lat(self):
        pass
