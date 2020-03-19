#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import werkzeug
import odoo
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class LogisticsSupplier(http.Controller):
    @http.route('/logistics_supplier_manage', auth="public", website=True)
    def show_logistics_supplier_manage(self):
        return request.render('website.logistics_supplier_manage')

