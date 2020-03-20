# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.osv import expression


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        RouteDelivery = request.env['route.network.delivery']

        quotation_count = RouteDelivery.search_count([
            ('vendor_id.partner_id', '=', partner.commercial_partner_id.id),
        ])

        values.update({
            'delivery_count': quotation_count,
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
            'from_location_id': {'label': _('From'), 'order': 'from_location_id'},
            'to_location_id': {'label': _('To'), 'order': 'to_location_id'},
            'unit_price': {'label': _('Price'), 'order': 'unit_price'},
        }

        # default sortby order
        if not sortby:
            sortby = 'from_location_id'
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