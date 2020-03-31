# -*- coding: utf-8 -*-

from odoo.addons.web.controllers import main as report
from odoo.http import content_disposition, route, request
from odoo import http
import requests
from odoo.http import request
import json
from odoo.tools import config
import logging
from pyecharts import options as opts
from pyecharts.charts import Geo, Bar
from pyecharts.globals import ChartType, SymbolType

_logger = logging.getLogger(__name__)


# 获取经纬度
def get_long_lat_value(name):
    if not name:
        return
    url = 'https://restapi.amap.com/v3/geocode/geo?parameters'
    parameters = {
        'address': name,
        'key': config.get('gaode_map_web_service_key')
    }
    _logger.info({
        'parameters': parameters
    })
    res = requests.get(url=url, params=parameters)
    if res.status_code == 200:
        geocodes_value = res.json().get('geocodes')[0] if res.json().get('geocodes', False) else False
        if not geocodes_value:
            return False, False
        location_info = geocodes_value.get('location')
        long_value, lat_value = location_info.split(',')
        return long_value, lat_value
    else:
        return False, False


def geo_lines(new_location_line) -> Geo:
    c = (
        Geo()
            .add_schema(maptype="china")
            .add_coordinate_json(json_file='location.json')
            .add(
            "geo",
            new_location_line,
            type_=ChartType.LINES,
            effect_opts=opts.EffectOpts(symbol=SymbolType.ARROW, symbol_size=6, color="purple"),
            linestyle_opts=opts.LineStyleOpts(curve=0.2),
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="Geo-Map-Lines"))
    )
    # c = (
    #     Geo()
    #     .add_schema(maptype="china")
    #     .add_coordinate_json(json_file=new_location_records)
    #     .add(
    #         "",
    #         [("广州", 55), ("北京", 66), ("杭州", 77), ("重庆", 88)],
    #         type_=ChartType.EFFECT_SCATTER,
    #         color="white",
    #     )
    #     .add(
    #         "geo",
    #         [("广州", "上海"), ("广州", "北京"), ("广州", "杭州"), ("广州", "重庆"), ("重庆", "北京")],
    #         type_=ChartType.LINES,
    #         effect_opts=opts.EffectOpts(
    #             symbol=SymbolType.ARROW, symbol_size=6, color="purple"
    #         ),
    #         linestyle_opts=opts.LineStyleOpts(curve=0.2),
    #     )
    #     .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    #     .set_global_opts(title_opts=opts.TitleOpts(title="Geo-Map-Lines"))
    # )

    # 返回 html
    # return c.render_embed()

    # 返回 json
    # return c.dump_options()
    # 但是无法加载

    return c.dump_options_with_quotes()


class GetNeededInfo(http.Controller):

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

    @http.route('/api/view_network/model_name/<string:model_name>/vendor_data/<int:record_id>', type="http",
                auth="none", methods=["GET"], csrf=False)
    def get_view_network_data(self, model_name=None, record_id=None, **post):

        if not record_id or not model_name:
            res = [
                ('成都', '北京'),
                ('成都', '新疆乌鲁木齐'),
                ('成都', '上海'),
                ('上海', '北京'),
                ('上海', '西藏')
            ]
            line_data = geo_lines(res)

            _logger.info({
                'line_data': line_data
            })
            return line_data
        else:
            # 获取数据
            model_id = request.env[model_name].sudo().browse(record_id)

            if not model_id:
                return False

            line_ids = model_id.line_ids

            res = []

            # 拼接
            for line_id in line_ids:
                res.append(
                    (line_id.from_warehouse_id.name, line_id.to_warehouse_id.name)
                )

            _logger.info({
                'res': res
            })

            res_lng_lat = self.get_all_location_lng_lat(line_ids)

            line_data = geo_lines(res)

            # _logger.info({
            #     'line_data': line_data
            # })
            return line_data

    # 获取所有位置的经纬度
    def get_all_location_lng_lat(self, line_ids):
        res = {}

        line_ids = line_ids.filtered(
            lambda x: not x.from_warehouse_id.location_long or not x.to_warehouse_id.location_long)

        all_from_warehouse = line_ids.mapped('from_warehouse_id')
        all_to_warehouse = line_ids.mapped('to_warehouse_id')
        all_warehouse_ids = list(set(all_from_warehouse + all_to_warehouse))

        for warehouse_id in all_warehouse_ids:
            warehouse_lng, warehouse_lnt = get_long_lat_value(warehouse_id.name)
            res[warehouse_id.name] = [warehouse_lng, warehouse_lnt]

        with open('location.json', 'w') as f:
            f.write(json.dumps(res))
        return res
