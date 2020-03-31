#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from werkzeug.exceptions import Forbidden, NotFound
from odoo import http, tools, fields
from odoo.http import request
from odoo.addons.sale.controllers.product_configurator import ProductConfiguratorController
import logging
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.website_sale_network.controllers.main import WebsiteSaleDeliveryNetwork

_logger = logging.getLogger(__name__)


PPG = 20  # Products Per Page
PPR = 4   # Products Per Row


class LogisticsShop(WebsiteSaleDeliveryNetwork):
    @http.route([
        '''/logistics_shop''',
        '''/logistics_shop/page/<int:page>''',
        '''/logistics_shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>''',
        '''/logistics_shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True)
    def logistics_shop(self, page=0, category=None, search='', ppg=False, **post):
        add_qty = int(post.get('add_qty', 1))
        if category:
            category = request.env['product.public.category'].search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()

        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        domain = self._get_search_domain(search, category, attrib_values)

        keep = QueryURL('/logistics_shop', category=category and int(category), search=search, attrib=attrib_list,
                        order=post.get('order'))

        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        url = "/logistics_shop"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        Product = request.env['product.template'].with_context(bin_size=True)

        Category = request.env['product.public.category']
        search_categories = False
        search_product = Product.search(domain)
        if search:
            categories = search_product.mapped('public_categ_ids')
            search_categories = Category.search(
                [('id', 'parent_of', categories.ids)] + request.website.website_domain())
            categs = search_categories.filtered(lambda c: not c.parent_id)
        else:
            categs = Category.search([('parent_id', '=', False)] + request.website.website_domain())

        parent_category_ids = []
        if category:
            url = "/logistics_shop/category/%s" % slug(category)
            parent_category_ids = [category.id]
            current_category = category
            while current_category.parent_id:
                parent_category_ids.append(current_category.parent_id.id)
                current_category = current_category.parent_id

        product_count = len(search_product)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        products = Product.search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            attributes = ProductAttribute.search([('attribute_line_ids.value_ids', '!=', False),
                                                  ('attribute_line_ids.product_tmpl_id', 'in', search_product.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        compute_currency = self._get_compute_currency(pricelist, products[:1])

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg),
            'rows': PPR,
            'categories': categs,
            'attributes': attributes,
            'compute_currency': compute_currency,
            'keep': keep,
            'parent_category_ids': parent_category_ids,
            'search_categories_ids': search_categories and search_categories.ids,
        }
        if category:
            values['main_object'] = category
        return request.render("website_logistics_shop.logistics_products", values)

    @http.route(['/logistics_shop/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def logistics_product(self, product, category='', search='', **kwargs):
        if not product.can_access_from_current_website():
            raise NotFound()

        add_qty = int(kwargs.get('add_qty', 1))

        product_context = dict(request.env.context, quantity=add_qty,
                               active_id=product.id,
                               partner=request.env.user.partner_id)
        ProductCategory = request.env['product.public.category']

        if category:
            category = ProductCategory.browse(int(category)).exists()

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attrib_set = {v[1] for v in attrib_values}

        keep = QueryURL('/logistics_shop', category=category and category.id, search=search, attrib=attrib_list)

        categs = ProductCategory.search([('parent_id', '=', False)])

        pricelist = request.website.get_current_pricelist()

        def compute_currency(price):
            return product.currency_id._convert(price, pricelist.currency_id,
                                                product._get_current_company(pricelist=pricelist,
                                                                             website=request.website),
                                                fields.Date.today())

        if not product_context.get('pricelist'):
            product_context['pricelist'] = pricelist.id
            product = product.with_context(product_context)

        values = {
            'search': search,
            'category': category,
            'pricelist': pricelist,
            'attrib_values': attrib_values,
            # compute_currency deprecated, get from product
            'compute_currency': compute_currency,
            'attrib_set': attrib_set,
            'keep': keep,
            'categories': categs,
            'main_object': product,
            'product': product,
            'add_qty': add_qty,
            'optional_product_ids': [p.with_context(active_id=p.id) for p in product.optional_product_ids],
            # get_attribute_exclusions deprecated, use product method
            'get_attribute_exclusions': self._get_attribute_exclusions,
        }
        return request.render("website_logistics_shop.logistics_product_info", values)

    @http.route(['/logistics_shop/sale_order'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def create_sale_order(self, **post):

        order = request.website.sale_get_order()
        _logger.info({
            'order': order
        })
        if post:
            from_location_name = post.get('from_location_name', False)
            to_location_name = post.get('to_location_name')
        _logger.info({
            'post': post
        })

        return request.redirect('/logistics_shop')

    @http.route(['/logistics/delivery_price'], type='json', auth='public', methods=['POST'], website=True, csrf=False)
    def get_logistics_delivery_price(self, **post):
        _logger.info({
            'post': post
        })
        if post:
            carrier_id = request.env['delivery.carrier'].browse(int(post.get('carrier_id')))
            from_location_name = post.get('from_location_name', False)
            to_location_name = post.get('to_location_name', False)

            _logger.info({
                'from_location_name': from_location_name,
                'to_location_name': to_location_name
            })
            from_warehouse_id, to_warehouse_id = self.find_correct_belong_position(
                from_location_name,
                to_location_name
            )

            price_total = carrier_id.get_price_from_netwrok_by_warehouse(from_warehouse_id, to_warehouse_id)

            return {
                'carrier_id': carrier_id.id,
                'success': True,
                'new_amount_delivery': price_total,
                'error_message': False,
                'warning_message': False
            }
