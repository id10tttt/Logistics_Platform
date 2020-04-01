#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    src_location_name = fields.Char('Source')
    dest_location_name = fields.Char('Dest')
