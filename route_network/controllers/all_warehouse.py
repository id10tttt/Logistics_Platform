# -*- coding: utf-8 -*-

from odoo.addons.web.controllers import main as report
from odoo.http import content_disposition, route, request
from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)


class GetAllWarehouse(http.Controller):

    @http.route('/api/warehouse/all_warehouse_line', type="http", auth="none", methods=["GET"], csrf=False)
    def get_all_warehouse_line(self, **post):
        """
        所有的有向线段
        虽有包含经纬度的位置
        :return: 所有线段，所有的位置
        """

        all_warehouse_obj = []

        # 所有位置
        all_warehouse_dict = {}
        all_warehouse_display_name = {}

        # 供应商合同
        all_supplier_contract = request.env['supplier.aop.contract'].sudo().search([])
        all_carrier_ids = all_supplier_contract.mapped('delivery_carrier_ids')

        all_warehouse_ids = [(x.from_warehouse_id, x.to_warehouse_id) for x in all_carrier_ids if
                            x.from_warehouse_id and x.to_warehouse_id]

        # 去除所有的合作伙伴位置
        all_warehouse_ids = [
            (x[0], x[1]) for x in all_warehouse_ids if
            not x[0].display_name.startswith('合作伙伴位置') and not x[1].display_name.startswith('合作伙伴位置')]

        # 所有线段
        all_line = [(x[0].id, x[1].id) for x in all_warehouse_ids]

        for x in all_warehouse_ids:
            all_warehouse_obj.append(x[0])
            all_warehouse_obj.append(x[1])

        all_warehouse_obj = list(set(all_warehouse_obj))

        for x in all_warehouse_obj:
            all_warehouse_dict[x.id] = x.name
            all_warehouse_display_name[x.id] = x.display_name

        return json.dumps({
            'all_line': all_line,
            'all_warehouse_dict': all_warehouse_dict,
            'all_warehouse_display_name': all_warehouse_display_name
        })
