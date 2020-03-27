#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import werkzeug
import odoo
from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class LogisticsManageWarehouse(http.Controller):
    @http.route('/logistics_warehouse_manage', auth="public", website=True, csrf=False)
    def show_logistics_warehouse_manage(self, *args, **kw):
        qcontext = self.get_qcontext()
        _logger.info({
            'qcontext': qcontext
        })
        if 'error' not in qcontext and request.httprequest.method == 'POST':
            warehouse_name = qcontext.get('warehouse_name')
            warehouse_code = qcontext.get('warehouse_code')
            warehouse_location_name = qcontext.get('warehouse_location_name')
            warehouse_service_area = qcontext.get('warehouse_service_area')

            current_partner_id = request.env.user.partner_id.id

            warehouse_obj = request.env['stock.warehouse'].sudo()
            warehouse_id = warehouse_obj.search([
                '|',
                ('partner_id', '=', current_partner_id),
                ('partner_id.parent_id', '=', current_partner_id),
                ('code', '=', warehouse_code)
            ])

            tmp_delivery_data = {
                'partner_id': current_partner_id,
                'name': warehouse_name,
                'code': warehouse_code,
                'service_area': warehouse_service_area,
            }

            if not warehouse_id:
                warehouse_id.create(tmp_delivery_data)
            else:
                warehouse_id.write(tmp_delivery_data)

            return request.render('website.logistics_warehouse_manage_success')

        return request.render('website.logistics_warehouse_manage')

    def get_qcontext(self):
        qcontext = request.params.copy()

        # Check
        values = {key: qcontext.get(key) for key in (
            'warehouse_name', 'warehouse_code', 'warehouse_location_name', 'warehouse_service_area')}
        if not values:
            raise UserError(_("The form was not properly filled in."))

        return qcontext

    @http.route('/logistics_warehouse_manage_success', auth="public", website=True, csrf=False)
    def logistics_supplier_manage_success(self, *args, **kw):
        return request.render('website.logistics_warehouse_manage_success')
