#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, api, fields


class RouteNetworkShortestPath(models.Model):
    _name = 'route.network.shortest.path'

    name = fields.Char('Path name')
    location_ids = fields.One2many('route.network.shortest.path.location', 'path_id', string='Path detail')


class RouteNetworkShortestPathLocation(models.Model):
    _name = 'route.network.shortest.path.location'
    _order = 'sequence'

    sequence = fields.Integer('Sequence', default=0)
    location_id = fields.Many2one('stock.location')
    path_id = fields.Many2one('route.network.shortest.path')
