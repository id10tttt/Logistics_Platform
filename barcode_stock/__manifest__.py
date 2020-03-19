# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
##########################################################################
{
    'name': 'Inventory Barcode Scanning',
    'summary': """
        This module adds support for barcodes scanning to the Inventory Management.
    """,
    'description': """https://webkul.com/blog/odoo-advanced-barcode-scanning
        This module adds support for barcodes scanning to the Inventory Management & will help you in pickings to make your process faster.
        Barcode Scanning, Product Scan, Scan, Scanning, Barcode, Stock Barcode, Picking Barcode, Delivery Barcode, Scan Module, Delivery Scan, Best Barcode Scanning Module
    """,
    'author': 'Webkul Software Pvt. Ltd.',
    'website': 'https://store.webkul.com/Odoo-Inventory-Barcode-Scanning.html',
    'license': 'Other proprietary',
    'category': 'Warehouse',
    'sequence': '10',
    'version': '1.0.0',
    'live_test_url': 'http://odoodemo.webkul.com/?module=barcode_stock&version=12.0',
    'depends': ['stock'],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'images': ['static/description/Banner.png'],
    'application': True,
    'pre_init_hook': 'pre_init_check',
    'price': 15,
    'currency': 'EUR',
}
