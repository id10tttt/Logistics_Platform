#!/usr/bin/env python3
# -*- cod utf-8 -*-

import matplotlib.pyplot as plt
import networkx as nx
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimSun', 'FangSong']
all_supplier_contract = self.env['supplier.aop.contract'].search([])
all_carrier_ids = all_supplier_contract.mapped('delivery_carrier_ids')

l_location_name = []
all_location_ids = [(x.from_location_id, x.to_location_id) for x in all_carrier_ids if
                    x.from_location_id and x.to_location_id]

all_location_ids = list(set(all_location_ids))

for x in all_location_ids:
    l_location_name.append(x[0].name)
    l_location_name.append(x[1].name)
l_location_name = set(l_location_name)
print(l_location_name)
all_location_ids = [(x[0].display_name, x[1].display_name) for x in all_location_ids if
                    not x[0].display_name.startswith('合作伙伴位置') and not x[1].display_name.startswith('合作伙伴位置')]
# print(len(all_location_ids), all_location_ids)
G = nx.Graph()
G.add_edges_from(all_location_ids)
nx.draw(G, with_labels=True, edge_color='b', node_color='g', node_size=1000)
plt.show()
# plt.savefig('/home/jx/Pictures/network.png', dpi=1080)