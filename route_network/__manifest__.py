# -*- encoding: utf-8 -*-
{
    'name': "Route network",
    'version': '12.0.0',
    'summary': 'Route network',
    'description': """Route network""",
    'author': '1di0t',
    "depends": ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/route_network.xml',
        'views/route_network_vendor.xml',
        'views/shortest_list_view.xml',
        'data/route_network.xml'
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
