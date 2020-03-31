#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Website(models.Model):
    _inherit = 'website'

    def get_all_delivery(self):
        delivery_ids = self.env['delivery.carrier'].sudo().search([])
        return delivery_ids
