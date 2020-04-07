#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OdooTestModel(models.Model):
    _name = 'odoo.test.model'

    name = fields.Char('Name')
