# -*- encoding: utf-8 -*-
{
    'name': "Odoo test",
    'version': '12.0.0',
    'summary': 'Odoo test',
    'description': """Odoo test""",
    'author': '1di0t',
    "depends": ['base', 'website'],
    'data': [
        'views/assets.xml',
        'security/ir.model.access.csv',
        'views/odoo_test_view.xml',
        # 'views/test_template.xml'
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
