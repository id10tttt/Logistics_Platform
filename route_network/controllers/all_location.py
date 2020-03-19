# -*- coding: utf-8 -*-

from odoo.addons.web.controllers import main as report
from odoo.http import content_disposition, route, request
from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)


class GetAllLocation(http.Controller):

    @http.route('/api/location/all_location_line', type="http", auth="none", methods=["GET"], csrf=False)
    def get_all_location_line(self, **post):
        """
        所有的有向线段
        虽有包含经纬度的位置
        :return: 所有线段，所有的位置
        """

        all_location_obj = []

        # 所有位置
        all_location_dict = {}
        all_location_display_name = {}

        # 供应商合同
        all_supplier_contract = request.env['supplier.aop.contract'].sudo().search([])
        all_carrier_ids = all_supplier_contract.mapped('delivery_carrier_ids')

        all_location_ids = [(x.from_location_id, x.to_location_id) for x in all_carrier_ids if
                            x.from_location_id and x.to_location_id]

        # 去除所有的合作伙伴位置
        all_location_ids = [
            (x[0], x[1]) for x in all_location_ids if
            not x[0].display_name.startswith('合作伙伴位置') and not x[1].display_name.startswith('合作伙伴位置')]

        # 所有线段
        all_line = [(x[0].id, x[1].id) for x in all_location_ids]

        for x in all_location_ids:
            all_location_obj.append(x[0])
            all_location_obj.append(x[1])

        all_location_obj = list(set(all_location_obj))

        for x in all_location_obj:
            all_location_dict[x.id] = x.name
            all_location_display_name[x.id] = x.display_name

        return json.dumps({
            'all_line': all_line,
            'all_location_dict': all_location_dict,
            'all_location_display_name': all_location_display_name
        })
