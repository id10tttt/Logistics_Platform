#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, api, fields
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp
import logging


_logger = logging.getLogger(__name__)


class RouteNetworkVendor(models.Model):
    _name = 'route.network.vendor'
    _sql_constraints = [
        ('unique_partner_id', 'unique(partner_id)', 'the partner(supplier) must be unique!')
    ]

    name = fields.Char('Name', required=True)
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)

    line_ids = fields.One2many('route.network.delivery', 'vendor_id', string='Line')


class RouteNetworkDelivery(models.Model):
    _name = 'route.network.delivery'
    _inherit = 'portal.mixin'

    vendor_id = fields.Many2one('route.network.vendor', ondelete='cascade', index=True)
    from_location_id = fields.Many2one('stock.location', string='From', required=True)
    to_location_id = fields.Many2one('stock.location', string='To', required=True)
    # unit_price = fields.Float('Price', digits=dp.get_precision('Price of delivery'), required=True)

    product_id = fields.Many2one('product.product', domain="[('type', '=', 'service')]", string='Product')
    type_id = fields.Many2one('route.network.delivery.type', string='Type')

    property_type_id = fields.Many2one('route.network.delivery.property.type', string='Property')
    property_amount = fields.Float('Amount')


class RouteNetworkDeliveryType(models.Model):
    _name = 'route.network.delivery.type'
    _sql_constraints = [
        ('unique_name', 'unique(name)', 'the name must be unique!')
    ]

    name = fields.Char('Name')


class RouteNetworkDeliveryPropertyType(models.Model):
    _name = 'route.network.delivery.property.type'
    _sql_constraints = [
        ('unique_name', 'unique(name)', 'the name must be unique!')
    ]

    name = fields.Char('Name')
