#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class StockWarehouse(models.Model):
    _name = 'stock.warehouse'
    _inherit = ['stock.warehouse', 'portal.mixin']

    # belong_partner_id = fields.Many2one('res.partner', 'Belong', default=lambda self: self.env.user.partner_id.id)
