#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LogisticsUserType(models.Model):
    _name = 'logistics.user.type'
    _sql_constraints = [
        ('unique_name_field_name', 'unique(name, field_name)', 'the name and field_name must be unique!')
    ]

    field_name = fields.Char('field')
    name = fields.Char('Name')

