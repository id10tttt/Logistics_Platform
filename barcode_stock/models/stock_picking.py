# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################


from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'barcodes.barcode_events_mixin']

    def on_barcode_scanned(self, barcode):
        product = self.env['product.product'].search(
            [('barcode', '=', barcode)])
        if product:
            moveLineObjs = self.move_line_ids_without_package.filtered(
                lambda r: r.product_id == product)
            moveLines = self.move_ids_without_package.filtered(
                lambda r: r.product_id == product)
            if moveLineObjs:
                for moveLineObj in moveLineObjs:
                    if moveLineObj.qty_done < moveLineObj.product_qty:
                        moveLineObj.qty_done += 1
                        break
                    elif moveLineObj == moveLineObjs[-1]:
                        raise UserError(
                            _('You are trying to deliver quantity more than ordered.'))
            elif moveLines:
                stateLabel = dict(
                    self.move_line_ids_without_package.fields_get('state')['state']['selection']).get(
                    moveLines[0].state, '')
                raise UserError(
                    _('Scanned product %s with barcode %s is present in this picking but currently in "%s" state.') %
                    (product.display_name, barcode, stateLabel))
            else:
                raise UserError(
                    _('This product %s with barcode %s is not present in this picking.') %
                    (product.name, barcode))
        else:
            raise UserError(
                _('This barcode %s is not related to any product.') %
                barcode)
