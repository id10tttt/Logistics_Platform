# -*- encoding: utf-8 -*-
{
    'name': "Website logistics shop",
    'summary': 'Website logistics shop',
    'description': """Website logistics shop""",
    'author': '1di0t',
    "depends": ['base', 'website', 'website_sale', 'auto_fill', 'route_network', 'stock', 'website_sale_network'],
    'data': [
        'views/assets.xml',
        'views/logistics_shop_template.xml'
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
