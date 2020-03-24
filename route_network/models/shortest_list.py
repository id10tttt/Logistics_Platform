#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, api, fields


class RouteNetworkShortestPath(models.Model):
    _name = 'route.network.shortest.path'

    name = fields.Char('Path name')
    warehouse_ids = fields.One2many('route.network.shortest.path.warehouse', 'path_id', string='Path detail')


class RouteNetworkShortestPathLocation(models.Model):
    _name = 'route.network.shortest.path.warehouse'
    _order = 'sequence'

    sequence = fields.Integer('Sequence', default=0)
    warehouse_id = fields.Many2one('stock.warehouse')
    path_id = fields.Many2one('route.network.shortest.path')
