#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, api, fields
import logging

_logger = logging.getLogger(__name__)


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    delivery_type = fields.Selection(selection_add=[('network', "Network")])
    network_id = fields.Many2one('route.network', 'Network')
