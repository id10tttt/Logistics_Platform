#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import werkzeug
import odoo
from odoo import http, _
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class LogisticsSupplier(http.Controller):
    @http.route('/logistics_supplier_manage', auth="public", website=True, csrf=False)
    def show_logistics_supplier_manage(self, *args, **kw):
        qcontext = self.get_qcontext()
        _logger.info({
            'qcontext': qcontext
        })
        if 'error' not in qcontext and request.httprequest.method == 'POST':
            current_partner_id = request.env.user.partner_id.id
            from_location_id = qcontext.get('from_location_id')
            to_location_id = qcontext.get('to_location_id')
            unit_price = qcontext.get('unit_price')

            current_partner_id = request.env.user.partner_id.id
            vendor_obj = request.env['route.network.vendor'].sudo()
            vendor_id = vendor_obj.search([
                ('partner_id', '=', current_partner_id)
            ])
            tmp_delivery_data = {
                'from_location_id': int(from_location_id),
                'to_location_id': int(to_location_id),
                'unit_price': float(unit_price)
            }

            vendor_id.write({
                'line_ids': [(0, 0, tmp_delivery_data)]
            })
            return request.render('website.logistics_supplier_manage_success')

        return request.render('website.logistics_supplier_manage')

    def get_qcontext(self):
        """ Shared helper returning the rendering context for signup and reset password """
        qcontext = request.params.copy()
        return qcontext

    @http.route('/logistics_supplier_manage_success', auth="public", website=True, csrf=False)
    def logistics_supplier_manage_success(self, *args, **kw):
        return request.render('website.logistics_supplier_manage_success')
