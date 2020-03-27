# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, http, _
from odoo import fields as odoo_fields
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
import logging

_logger = logging.getLogger(__name__)


class CustomerPortal(CustomerPortal):

    def _get_archive_groups(self, model, domain=None, fields=None, groupby="create_date", order="create_date desc", sudo=None):
        if not sudo:
            return super(CustomerPortal, self)._get_archive_groups(model, domain, fields, groupby, order)
        else:
            if not model:
                return []
            if domain is None:
                domain = []
            if fields is None:
                fields = ['name', 'create_date']
            groups = []

            groups_ids = request.env[model].sudo()._read_group_raw(domain, fields=fields, groupby=groupby, orderby=order)
            for group in groups_ids:
                dates, label = group[groupby]
                date_begin, date_end = dates.split('/')
                groups.append({
                    'date_begin': odoo_fields.Date.to_string(odoo_fields.Date.from_string(date_begin)),
                    'date_end': odoo_fields.Date.to_string(odoo_fields.Date.from_string(date_end)),
                    'name': label,
                    'item_count': group[groupby + '_count']
                })
            return groups

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        RouteDelivery = request.env['route.network.delivery']
        stock_warehouse_obj = request.env['stock.warehouse'].sudo()
        quotation_count = RouteDelivery.search_count([
            ('vendor_id.partner_id', '=', partner.commercial_partner_id.id),
        ])
        warehouse_count = stock_warehouse_obj.search_count([
            '|',
            ('partner_id', '=', partner.commercial_partner_id.id),
            ('partner_id.parent_id', '=', partner.commercial_partner_id.id)
        ])
        values.update({
            'delivery_count': quotation_count,
            'warehouse_count': warehouse_count
        })
        return values

    # 运力
    @http.route(['/my/delivery_manage', '/my/delivery_manage/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_delivery_manage(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        RouteDelivery = request.env['route.network.delivery']

        domain = [
            ('vendor_id.partner_id', '=', partner.commercial_partner_id.id),
        ]

        searchbar_sortings = {
            'from_warehouse_id': {'label': _('From'), 'order': 'from_warehouse_id'},
            'to_warehouse_id': {'label': _('To'), 'order': 'to_warehouse_id'},
            'unit_price': {'label': _('Price'), 'order': 'unit_price'},
        }

        # default sortby order
        if not sortby:
            sortby = 'from_warehouse_id'
        sort_order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('route.network.delivery', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        delivery_count = RouteDelivery.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/delivery_manage",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=delivery_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        delivery_ids = RouteDelivery.sudo().search(domain, order=sort_order, limit=self._items_per_page,
                                             offset=pager['offset'])

        request.session['my_quotations_history'] = delivery_ids.ids[:100]

        values.update({
            'date': date_begin,
            'delivery_ids': delivery_ids.sudo(),
            'page_name': 'delivery',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/delivery_manage',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("website_vendor.portal_my_delivery_id", values)

    # 仓库信息
    @http.route(['/my/warehouse_manage', '/my/warehouse_manage/page/<int:page>'], type='http', auth="user",
                website=True)
    def portal_my_warehouse_manage(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        stock_warehouse_obj = request.env['stock.warehouse'].sudo()

        domain = [
            '|',
            ('partner_id', '=', partner.commercial_partner_id.id),
            ('partner_id.parent_id', '=', partner.commercial_partner_id.id)
        ]

        searchbar_sortings = {
            'name': {'label': _('Name'), 'order': 'name'},
            'code': {'label': _('Code'), 'order': 'code'},
            'location_name': {'label': _('Location'), 'order': 'location_name'},
        }

        # default sortby order
        if not sortby:
            sortby = 'name'
        sort_order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('stock.warehouse', domain, sudo=True)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        warehouse_count = stock_warehouse_obj.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/warehouse_manage",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=warehouse_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        warehouse_ids = stock_warehouse_obj.search(domain, order=sort_order, limit=self._items_per_page,
                                                   offset=pager['offset'])

        request.session['my_quotations_history'] = warehouse_ids.ids[:100]

        values.update({
            'date': date_begin,
            'warehouse_ids': warehouse_ids.sudo(),
            'page_name': 'delivery',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/warehouse_manage',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("website_vendor.portal_my_warehouse_id", values)

    @http.route(['/manage/warehouse/edit', '/manage/warehouse/edit/<int:warehouse_id>'], type='http', auth='user',
                website=True)
    def edit_warehouse(self, warehouse_id=None, redirect=None, **post):
        values = self._prepare_portal_layout_values()

        warehouse_id = request.env['stock.warehouse'].sudo().browse(warehouse_id)
        values.update({
            'error': {},
            'error_message': [],
        })

        if post:
            update_value = {
                'name': post.get('warehouse_name'),
                'code': post.get('warehouse_code'),
                'location_name': post.get('location_name'),
                'service_area': post.get('service_area')
            }
            _logger.info({
                'update_value': update_value
            })
            warehouse_id.sudo().write(update_value)
            return request.redirect('/my/warehouse_manage')

        if not warehouse_id:
            warehouse_id = request.env['stock.warehouse'].sudo().browse(1)

        values.update({
            'warehouse_id': warehouse_id,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_warehouse_details',
        })

        response = request.render("website_vendor.portal_my_warehouse_details", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @http.route(['/manage/warehouse/delete', '/manage/warehouse/delete/<int:warehouse_id>'], type='http', auth='user',
                website=True)
    def delete_warehouse(self, warehouse_id=None, redirect=None, **post):
        warehouse_id = request.env['stock.warehouse'].sudo().browse(warehouse_id)
        warehouse_id.write({
            'active': False
        })
        return request.redirect('/my/warehouse_manage')
