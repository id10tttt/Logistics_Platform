# -*- encoding: utf-8 -*-
{
    'name': "Website sale network",
    'version': '12.0.0',
    'summary': 'Website sale network',
    'description': """Website sale network""",
    'author': '1di0t',
    "depends": ['base', 'website', 'website_sale', 'website_sale_delivery', 'sale', 'stock'],
    'data': [
        'views/sale_delivery_templates.xml',
        'views/sale_order.xml',
        'views/stock_warehouse.xml',
        'views/res_partner.xml',
        'views/assets.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
