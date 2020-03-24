#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, api, fields
from odoo.exceptions import UserError
from ..tools import dijkstras
import logging
import matplotlib.pyplot as plt
import networkx as nx
import traceback
import random

_logger = logging.getLogger(__name__)


class RouteNetwork(models.Model):
    _name = 'route.network'

    _sql_constraints = [
        ('unique_partner_id', 'unique(partner_id)', 'the partner must be unique!')
    ]

    name = fields.Char('Name')
    partner_id = fields.Many2one('res.partner', 'Partner')
    product_id = fields.Many2one('product.product', domain="[('type', '=', 'service')]", string='Product')
    step_ids = fields.One2many(
        comodel_name='route.network.step',
        inverse_name='network_id',
        string='Network',
        ondelete='cascade',
        help='Network.')

    shortest_note = fields.Text('Shortest')
    shortest_weight = fields.Float('Dijkstra length')

    start_warehouse_id = fields.Many2one('stock.warehouse', 'Start')
    end_warehouse_id = fields.Many2one('stock.warehouse', 'End')

    network_image = fields.Binary('Network', attachment=True)

    path_id = fields.Many2one('route.network.shortest.path', 'Path')
    route_id = fields.Many2one('stock.location.route', 'Route')

    def parse_from_to_warehouse(self):
        warehouse_ids = self.path_id.warehouse_ids.mapped('warehouse_id')
        pair_warehouse_ids = []
        for index_l, value in enumerate(warehouse_ids):
            if index_l + 1 >= len(warehouse_ids):
                continue
            pair_warehouse_ids.append(
                (warehouse_ids[index_l], warehouse_ids[index_l + 1])
            )
        return pair_warehouse_ids

    def parse_warehouse_route_value(self, warehouse_ids):
        values = []
        index_warehouse = True
        for warehouse_id in warehouse_ids:
            from_id = warehouse_id[0]
            to_id = warehouse_id[1]

            from_step_id = self.step_ids.filtered(lambda x: x.warehouse_id.id == from_id.id)
            to_step_id = self.step_ids.filtered(lambda x: x.warehouse_id.id == to_id.id)

            rule_id = self.env['route.network.rule'].search([
                ('from_id', 'in', from_step_id.ids),
                ('to_id', 'in', to_step_id.ids),
            ])
            if not rule_id:
                raise UserError('Error!')

            # 使用供应商合同条款(carrier_id)里面的picking_type_id
            # rule_id.list_ids[0].carrier_id.picking_type_id.id
            tmp = {
                'action': 'pull',
                'name': from_id.display_name + ' -> ' + to_id.display_name,
                'warehouse_src_id': from_id.id,
                'warehouse_id': to_id.id,
                'picking_type_id': rule_id.list_ids[0].carrier_id.picking_type_id.id
            }
            if index_warehouse:
                tmp.update({
                    'procure_method': 'make_to_stock'
                })
                index_warehouse = False
            else:
                tmp.update({
                    'procure_method': 'make_to_order'
                })
            values.append((0, 0, tmp))
        return values

    @api.multi
    def generate_stock_warehouse_route_line(self):
        self.ensure_one()
        if self.path_id:
            warehouse_ids = self.parse_from_to_warehouse()

            line_values = self.parse_warehouse_route_value(warehouse_ids)

            start_warehouse_id = self.path_id.warehouse_ids[0].warehouse_id
            end_warehouse_id = self.path_id.warehouse_ids[-1].warehouse_id

            route_value = {
                'name': start_warehouse_id.display_name + ' -> ' + end_warehouse_id.display_name,
                'sale_selectable': True,
                'rule_ids': line_values
            }
            _logger.info({
                'route_value': route_value
            })
            res = self.env['stock.location.route'].create(route_value)
            self.route_id = res.id

    def find_out_all_simple_path_by_networkx(self, network_x_g, all_rule_ids):
        tmp_node = [(x[0].id, x[1].id, x[2]) for x in all_rule_ids]

        tmp_node = list(set(tmp_node))

        network_x_g.add_weighted_edges_from(tmp_node)

        source_id = self.start_warehouse_id.id
        target_id = self.end_warehouse_id.id

        shortest_path = nx.all_simple_paths(network_x_g, source=source_id, target=target_id)
        return shortest_path

    def create_shortest_list_path(self, all_simple_path):
        """
            model: route.network.shortest.path
        :param all_simple_path:
        :return:
        """

        # delete first
        self.env['route.network.shortest.path'].search([]).unlink()

        data = []
        for simple_path_id in list(all_simple_path):
            warehouse_ids = self.env['stock.warehouse'].browse(simple_path_id)
            name = ' ->'.join(x.display_name for x in warehouse_ids)
            tmp = [(0, 0, {
                'warehouse_id': x.id
            }) for x in warehouse_ids]

            data.append({
                'name': name,
                'warehouse_ids': tmp
            })

        res = self.env['route.network.shortest.path'].create(data)
        _logger.info({
            'create': res
        })

    def find_out_shortest_path_with_networkx(self, from_warehouse_id=None, to_warehouse_id=None):
        """
        dijkstra_path_length
            Returns the shortest weighted path length in G from source to target.
        dijkstra_path
            Returns the shortest weighted path from source to target in G.
        all_simple_paths
            Generate all simple paths in the graph G from source to target.
        shortest_path
            Compute shortest paths in the graph.
        :return:
        """
        try:
            # 初始化
            network_x_g = nx.DiGraph()

            if not self.step_ids:
                raise UserError('Empty >> _ << ')

            # 获取所有的箭头
            all_rule_ids = self.step_ids.mapped('out_transition_ids') + self.step_ids.mapped('in_transition_ids')

            # all_rule_ids = [(x.from_id, x.to_id, x.quantity_weight) for x in all_rule_ids]
            all_rule_ids = [(x.from_id.warehouse_id, x.to_id.warehouse_id, x.quantity_weight) for x in all_rule_ids]

            # 去重
            all_rule_ids = list(set(all_rule_ids))

            # 所有节点的信息，包括权重
            tmp_node = [(x[0].display_name, x[1].display_name, x[2]) for x in all_rule_ids]

            tmp_node = list(set(tmp_node))

            network_x_g.add_weighted_edges_from(tmp_node)
            #
            source_id = self.start_warehouse_id.display_name
            target_id = self.end_warehouse_id.display_name

            if from_warehouse_id and to_warehouse_id:
                source_id = from_warehouse_id.display_name
                target_id = to_warehouse_id.display_name

            if not network_x_g.has_node(source_id) or not network_x_g.has_node(target_id):
                return

            shortest_path = nx.shortest_path(network_x_g, source=source_id, target=target_id)
            # shortest_path = nx.all_simple_paths(network_x_g, source=source_id, target=target_id)

            # shortest_path = self.find_out_all_simple_path_by_networkx(network_x_g, all_rule_ids)
            #
            # self.create_shortest_list_path(shortest_path)
            # # Returns the shortest weighted path length in G from source to target.
            shortest_dijkstra_path_length = nx.dijkstra_path_length(network_x_g, source=source_id, target=target_id)

            # shortest_path = nx.shortest_path_length(network_x_g, source=source_id, target=target_id)
            # shortest_path = nx.shortest_path_length(network_x_g)

            # shortest_note = ' -> '.join(x for x in shortest_path)
            # self.shortest_note = shortest_note

            self.shortest_weight = shortest_dijkstra_path_length if shortest_dijkstra_path_length else 0.0
            self.shortest_note = list(shortest_path) if shortest_path else False
        except Exception as e:
            raise UserError(e)

    def find_out_shortest_path(self):
        if not self.step_ids:
            raise UserError('Empty >> _ << ')
        all_warehouse_ids = self.step_ids.mapped('warehouse_id')
        all_warehouse_name = {
            x.id: x.display_name for x in all_warehouse_ids
        }
        all_warehouse_ids = list(set(all_warehouse_ids.ids))

        # 获取所有的箭头
        all_rule_ids = self.step_ids.mapped('out_transition_ids') + self.step_ids.mapped('in_transition_ids')

        # 找到最开始的节点和最后的节点
        start_rule_id = self.step_ids.filtered(lambda x: not x.out_transition_ids)
        end_rule_id = self.step_ids.filtered(lambda x: not x.in_transition_ids)

        # 注册所有的节点
        all_node = []
        warehouse_node = {}
        for warehouse_id in all_warehouse_ids:
            node_id = dijkstras.Node(warehouse_id)
            warehouse_node[warehouse_id] = node_id
            all_node.append(node_id)

        # 初始化
        node_graph = dijkstras.Graph(all_node)

        # 添加节点信息
        for warehouse_id in all_warehouse_ids:
            # 找到该节点的所有开始
            from_rules = all_rule_ids.filtered(lambda x: x.from_id.warehouse_id.id == warehouse_id)
            if not from_rules:
                continue
            for from_rule_id in from_rules:
                # 找到节点
                from_node = warehouse_node.get(from_rule_id.from_id.warehouse_id.id)
                to_node = warehouse_node.get(from_rule_id.to_id.warehouse_id.id)

                # 连接 有方向的连接
                node_graph.directed_connect(from_node, to_node, from_rule_id.quantity_weight)

                # 无方向的连接
                # node_graph.connect(from_node, to_node, from_rule_id.quantity_weight)

        end_node = warehouse_node.get(end_rule_id.warehouse_id.id)

        res = [(weight, [n.data for n in node]) for (weight, node) in node_graph.dijkstra(end_node)]
        res = res[-1][-1]

        shortest_note = ' -> '.join(all_warehouse_name.get(x) for x in res)

        self.shortest_note = shortest_note
        _logger.info({
            'path': [(weight, [n.data for n in node]) for (weight, node) in node_graph.dijkstra(end_node)]
        })

    def generate_all_customer_contract_network(self):
        """
            根据所有的客户合同，生成一个大的网络
        """
        all_start_end_warehouse = self.find_all_start_end_warehouse(model_name='customer.aop.contract')

        # 获取所有开始，结束位置，以及条款
        all_start_end_warehouse = self.find_out_all_start_end_warehouse_by_weight(model_name='customer.aop.contract')
        self.create_all_warehouse_steps(all_start_end_warehouse)

        self.generate_route_by_warehouse(all_start_end_warehouse)

    def generate_all_supplier_contract_network(self):
        """
            根据所有的供应商合同，生成一个大的网络
        """
        all_start_end_warehouse = self.find_all_start_end_warehouse(model_name='supplier.aop.contract')

        # 获取所有开始，结束位置，以及条款
        all_start_end_warehouse = self.find_out_all_start_end_warehouse_by_weight(model_name='supplier.aop.contract')

        self.create_all_warehouse_steps(all_start_end_warehouse)

        self.generate_route_by_warehouse(all_start_end_warehouse)
        # self.generate_route_by_warehouse_with_weight(all_start_end_warehouse)

    # 获取所有线路
    def generate_all_delivery_network(self):
        """
        生成运力网络
        :return:
        """
        # 获取所有开始，结束位置，以及条款
        all_start_end_warehouse = self.find_out_all_start_end_warehouse_from_delivery(model_name='route.network.vendor')

        self.create_all_warehouse_steps(all_start_end_warehouse)

        self.generate_route_by_warehouse(all_start_end_warehouse)

    # 生成点
    def create_all_warehouse_steps(self, all_start_end_warehouse):
        all_warehouse_ids = []
        for x in all_start_end_warehouse:
            all_warehouse_ids += list(x)[:2]

        # 所有位置
        all_warehouse_ids = list(set(all_warehouse_ids))
        all_warehouse_ids = self.env['stock.warehouse'].browse(all_warehouse_ids)

        data = []
        for x in all_warehouse_ids:
            data.append({
                'name': x.display_name,
                'warehouse_id': x.id
            })

        # delete first
        # self.step_ids.unlink()

        all_ids = self.env['route.network.step'].create(data)

        self.step_ids = [(6, 0, all_ids.ids)]

    def generate_route_by_warehouse_with_weight(self, warehouse_ids):
        """
            生成线段
            :param warehouse_ids: 所有开始和结束节点
            :return:
        """
        all_steps = self.step_ids
        data = []
        for warehouse_id in warehouse_ids:
            from_step = all_steps.filtered(lambda x: x.warehouse_id.id == warehouse_id[0])
            to_step = all_steps.filtered(lambda x: x.warehouse_id.id == warehouse_id[1])

            if not from_step or not to_step:
                continue

            data.append({
                'from_id': from_step.id,
                'to_id': to_step.id,
                'quantity_weight': warehouse_id[2]
            })
        # empty first
        # self.step_ids.mapped('out_transition_ids').unlink()
        # self.step_ids.mapped('in_transition_ids').unlink()

        res = self.env['route.network.rule'].create(data)

    def generate_route_by_warehouse(self, warehouse_ids):
        """
            生成线段
        :param warehouse_ids: 所有开始和结束节点
        :return:
        """
        all_steps = self.step_ids
        data = []
        for warehouse_id in warehouse_ids:
            from_step = all_steps.filtered(lambda x: x.warehouse_id.id == warehouse_id[0])
            to_step = all_steps.filtered(lambda x: x.warehouse_id.id == warehouse_id[1])

            if not from_step or not to_step:
                continue

            quantity_weight = 0
            tmp_carrier_data = []
            all_carrier_ids = warehouse_id[2]

            # 价格列表
            for x in all_carrier_ids.keys():
                tmp_carrier_data.append(
                    (0, 0, {
                        # 'carrier_id': int(x),
                        'delivery_id': int(x),
                        'quantity_weight': all_carrier_ids.get(x)
                    })
                )
                quantity_weight += all_carrier_ids.get(x)

            quantity_weight = quantity_weight / len(all_carrier_ids.keys())
            data.append({
                'from_id': from_step.id,
                'to_id': to_step.id,
                'list_ids': tmp_carrier_data,
                'quantity_weight': round(float(quantity_weight) * 1000, -1) / 1000
            })

        # empty first
        # self.step_ids.mapped('out_transition_ids').unlink()
        # self.step_ids.mapped('in_transition_ids').unlink()

        res = self.env['route.network.rule'].create(data)

    def find_all_start_end_warehouse_with_weight(self, model_name=False):
        all_supplier_contract = self.env[model_name].search([])
        all_carrier_ids = all_supplier_contract.mapped('delivery_carrier_ids')

        if model_name == 'supplier.aop.contract':
            all_warehouse_ids = [
                (x.from_warehouse_id, x.to_warehouse_id, x.product_standard_price) for x in all_carrier_ids
                if x.from_warehouse_id and x.to_warehouse_id]
        elif model_name == 'customer.aop.contract':
            all_warehouse_ids = [(x.from_warehouse_id, x.to_warehouse_id, x.fixed_price) for x in all_carrier_ids
                                if x.from_warehouse_id and x.to_warehouse_id]

        # all_warehouse_ids = [(x.from_warehouse_id, x.to_warehouse_id) for x in all_carrier_ids
        #                     if x.from_warehouse_id and x.to_warehouse_id]

        # 去重
        all_warehouse_ids = list(set(all_warehouse_ids))

        all_warehouse_ids = [(x[0].id, x[1].id, round(float(x[2]) * 1000, -1) / 1000) for x in all_warehouse_ids if
                            not x[0].display_name.startswith('合作伙伴位置') and
                            not x[1].display_name.startswith('合作伙伴位置')]
        return all_warehouse_ids

    def format_start_end_warehouse_value(self, all_warehouse_ids, model_name):
        """
        # {
        #     'a,b': {1: 1, 2: 3}
        # }
        :param all_warehouse_ids:
        :param model_name:
        :return: [('a', 'b', {1: 1, 2: 3})...]
        """
        res = {}
        for x in all_warehouse_ids:
            tmp_key = str(x[0].id) + ',' + str(x[1].id)
            if model_name == 'supplier.aop.contract':
                tmp_price = round(float(x[2].product_standard_price) * 1000, -1) / 1000
            elif model_name == 'customer.aop.contract':
                tmp_price = round(float(x[2].fixed_price) * 1000, -1) / 1000
            elif model_name == 'route.network.vendor':
                tmp_price = round(float(x[2].unit_price) * 1000, -1) / 1000

            if tmp_key in res:
                tmp_value = res.get(tmp_key)
                tmp_value.update({
                    x[2].id: tmp_price
                })
                res[tmp_key] = tmp_value
            else:
                res[tmp_key] = {
                    x[2].id: tmp_price
                }
        values = []
        for x in res.keys():
            start_id, end_id = x.split(',')
            values.append(
                (int(start_id), int(end_id), res.get(x))
            )
        return values

    # 查找所有的位置
    def find_out_all_start_end_warehouse_by_weight(self, model_name=False):
        """
        :param model_name: supplier.aop.contract or customer.aop.contract
        :return: [(start, end, {})...]
        """
        all_supplier_contract = self.env[model_name].search([])
        all_carrier_ids = all_supplier_contract.mapped('delivery_carrier_ids')

        all_warehouse_ids = [(x.from_warehouse_id, x.to_warehouse_id, x) for x in all_carrier_ids
                            if x.from_warehouse_id and x.to_warehouse_id]

        # 去除所有的合作伙伴位置
        all_warehouse_ids = [(x[0], x[1], x[2]) for x in all_warehouse_ids if
                            not x[0].display_name.startswith('合作伙伴位置') and
                            not x[1].display_name.startswith('合作伙伴位置')]


        all_warehouse_ids = list(set(all_warehouse_ids))

        res = self.format_start_end_warehouse_value(all_warehouse_ids, model_name)

        return res

    # 查找所有的位置 - 运力
    def find_out_all_start_end_warehouse_from_delivery(self, model_name=False):
        """
        :param model_name: supplier.aop.contract or customer.aop.contract
        :return: [(start, end, {})...]
        """
        all_vendor_id = self.env[model_name].search([
            ('partner_id', '=', self.partner_id.id)
        ])
        if not all_vendor_id:
            raise UserError('Not found!')

        all_delivery_ids = all_vendor_id.mapped('line_ids')

        if not all_delivery_ids:
            raise UserError('Not found delivery info !')

        all_warehouse_ids = [(x.from_warehouse_id, x.to_warehouse_id, x) for x in all_delivery_ids
                            if x.from_warehouse_id and x.to_warehouse_id]

        # 去除所有的合作伙伴位置
        all_warehouse_ids = [(x[0], x[1], x[2]) for x in all_warehouse_ids if
                            not x[0].display_name.startswith('合作伙伴位置') and
                            not x[1].display_name.startswith('合作伙伴位置')]

        all_warehouse_ids = list(set(all_warehouse_ids))

        res = self.format_start_end_warehouse_value(all_warehouse_ids, model_name)

        return res

    def find_all_start_end_warehouse(self, model_name=False):
        """
            查找所有的线段，去重
        """
        all_supplier_contract = self.env[model_name].search([])
        all_carrier_ids = all_supplier_contract.mapped('delivery_carrier_ids')

        all_warehouse_ids = [(x.from_warehouse_id, x.to_warehouse_id) for x in all_carrier_ids
                            if x.from_warehouse_id and x.to_warehouse_id]

        # 去重
        all_warehouse_ids = list(set(all_warehouse_ids))

        all_warehouse_ids = [(x[0].id, x[1].id) for x in all_warehouse_ids if
                            not x[0].display_name.startswith('合作伙伴位置') and
                            not x[1].display_name.startswith('合作伙伴位置')]

        return all_warehouse_ids

    # 重定向到 maps
    def show_route_network_maps(self):
        url = 'http://47.103.54.14/:8889'
        return {
            'type': 'ir.actions.act_url',
            'url': url
        }


class RouteNetworkStep(models.Model):
    _name = 'route.network.step'

    network_id = fields.Many2one('route.network', ondelete='cascade', index=True)
    name = fields.Char('Name')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')

    out_transition_ids = fields.One2many(
        comodel_name='route.network.rule',
        inverse_name='from_id',
        string='From',
        ondelete='cascade')
    in_transition_ids = fields.One2many(
        comodel_name='route.network.rule',
        inverse_name='to_id',
        string='To',
        ondelete='cascade')


class RouteNetworkRule(models.Model):
    _name = 'route.network.rule'
    _order = 'sequence'

    name = fields.Char('Name', compute='_compute_name')

    sequence = fields.Integer(
        string='Sequence',
        default=0,
        required=False,
        help='Sequence order.')

    from_id = fields.Many2one('route.network.step', ondelete='cascade', index=True)
    to_id = fields.Many2one('route.network.step', ondelete='cascade', index=True)

    quantity_weight = fields.Float('Weight')

    list_ids = fields.One2many('route.network.rule.list', 'rule_id', string='Rule list')

    @api.multi
    @api.depends('from_id', 'to_id')
    def _compute_name(self):
        for line_id in self:
            if line_id.from_id and line_id.to_id:
                line_id.name = line_id.from_id.name + ' -> ' + line_id.to_id.name


class RouteNetworkRuleList(models.Model):
    _name = 'route.network.rule.list'
    _description = 'Rule list'

    rule_id = fields.Many2one('route.network.rule', string='Rule', ondelete='cascade', index=True)
    # carrier_id = fields.Many2one('delivery.carrier', 'Carrier')
    delivery_id = fields.Many2one('route.network.delivery', 'Delivery')
    quantity_weight = fields.Float('Weight')
