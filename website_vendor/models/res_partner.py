#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    user_type = fields.Selection(
        [('logistics_supplier', 'Logistics Supplier'),
         ('logistics_user', 'Logistics User')], string="User Type",
        copy=False, track_visibility='onchange')
