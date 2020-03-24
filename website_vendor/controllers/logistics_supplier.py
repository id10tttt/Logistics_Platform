#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import werkzeug
import odoo
from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class LogisticsSupplier(http.Controller):
    @http.route('/logistics_supplier_manage', auth="public", website=True, csrf=False)
    def show_logistics_supplier_manage(self, *args, **kw):
        qcontext = self.get_qcontext()

        # service_product_ids = request.env['product.product'].sudo().search([('type', '=', 'service')])
        delivery_type = request.env['route.network.delivery.type'].sudo().search([])
        property_type = request.env['route.network.delivery.property.type'].sudo().search([])

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            from_warehouse_id = qcontext.get('from_warehouse_id')
            to_warehouse_id = qcontext.get('to_warehouse_id')
            # property_amount = qcontext.get('property_amount')
            product_id = qcontext.get('service_product_id')
            type_id = qcontext.get('delivery_type_id')
            property_type_id = qcontext.get('property_type_id')

            current_partner_id = request.env.user.partner_id.id
            vendor_obj = request.env['route.network.vendor'].sudo()
            vendor_id = vendor_obj.search([
                ('partner_id', '=', current_partner_id)
            ])
            if not vendor_id:
                vendor_id = vendor_obj.create({
                    'name': request.env.user.partner_id.name,
                    'partner_id': current_partner_id
                })
                _logger.info({
                    'create': vendor_id
                })

            tmp_delivery_data = {
                'from_warehouse_id': int(from_warehouse_id),
                'to_warehouse_id': int(to_warehouse_id),
                'unit_price': 0.0,
                # 'product_id': int(product_id),
                'type_id': int(type_id),
                'property_type_id': int(property_type_id),
                # 'property_amount': float(property_amount)
            }

            vendor_id.write({
                'line_ids': [(0, 0, tmp_delivery_data)]
            })
            return request.render('website.logistics_supplier_manage_success')

        return request.render('website.logistics_supplier_manage', {
            # 'service_product_ids': service_product_ids,
            'delivery_type': delivery_type,
            'property_type': property_type
        })

    def get_qcontext(self):
        qcontext = request.params.copy()

        # Check
        values = {key: qcontext.get(key) for key in (
            'from_warehouse_id', 'to_warehouse_id', 'delivery_type_id', 'property_type_id')}
        if not values:
            raise UserError(_("The form was not properly filled in."))

        return qcontext

    @http.route('/logistics_supplier_manage_success', auth="public", website=True, csrf=False)
    def logistics_supplier_manage_success(self, *args, **kw):
        return request.render('website.logistics_supplier_manage_success')
