# -*- encoding: utf-8 -*-
{
    'name': "Route network",
    'version': '12.0.0',
    'summary': 'Route network',
    'description': """Route network""",
    'author': '1di0t',
    "depends": ['base', 'stock', 'portal', 'product'],
    'data': [
        'views/assets.xml',
        'security/ir.model.access.csv',
        'views/route_network.xml',
        'views/route_network_vendor.xml',
        'views/shortest_list_view.xml',
        'data/route_network.xml',
        'data/property_type.xml'
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
