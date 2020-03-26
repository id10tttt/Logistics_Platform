#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import config


class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    def get_param_from_config_file(self, key_name):
        return config.get(key_name, False)
