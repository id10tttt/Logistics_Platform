# -*- encoding: utf-8 -*-
{
    'name': "Website vendor",
    'version': '12.0.0',
    'summary': 'Website vendor',
    'description': """Website vendor""",
    'author': '1di0t',
    "depends": ['base', 'website', 'auth_signup', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'security/website_vendor.xml',
        'views/asset.xml',
        'views/website_signup.xml',
        'views/res_partner.xml',
        'data/logistics_user_type.xml',
        'views/logistics_supplier.xml',
        'views/logistics_manage.xml',
        'views/logistics_portal_templates.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}