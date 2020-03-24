#!/usr/bin/env python3
# -*- cod utf-8 -*-

import matplotlib.pyplot as plt
import networkx as nx
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimSun', 'FangSong']
all_supplier_contract = self.env['supplier.aop.contract'].search([])
all_carrier_ids = all_supplier_contract.mapped('delivery_carrier_ids')

l_warehouse_name = []
all_warehouse_ids = [(x.from_warehouse_id, x.to_warehouse_id) for x in all_carrier_ids if
                    x.from_warehouse_id and x.to_warehouse_id]

all_warehouse_ids = list(set(all_warehouse_ids))

for x in all_warehouse_ids:
    l_warehouse_name.append(x[0].name)
    l_warehouse_name.append(x[1].name)
l_warehouse_name = set(l_warehouse_name)
print(l_warehouse_name)
all_warehouse_ids = [(x[0].display_name, x[1].display_name) for x in all_warehouse_ids if
                    not x[0].display_name.startswith('合作伙伴位置') and not x[1].display_name.startswith('合作伙伴位置')]
# print(len(all_warehouse_ids), all_warehouse_ids)
G = nx.Graph()
G.add_edges_from(all_warehouse_ids)
nx.draw(G, with_labels=True, edge_color='b', node_color='g', node_size=1000)
plt.show()
# plt.savefig('/home/jx/Pictures/network.png', dpi=1080)
