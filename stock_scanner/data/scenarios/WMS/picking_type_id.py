'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

# 清除步骤
terminal.clean_tmp_values(['picking_type_name'])

filter_clean_keys = [
    'warehouse_id',
    'warehouse_code',
    'warehouse_name',
]
warehouse_id = message
# 判断仓库id和缓存中的仓库id 是否一致,不一致代表仓库切换过了
cache_warehouse_id = terminal.get_tmp_value('warehouse_id', False)
if warehouse_id != cache_warehouse_id:
    # 清除原有的仓库缓存信息
    terminal.clean_tmp_values(filter_clean_keys)

    domain = [('id', '=', warehouse_id)]
    warehouse = env['stock.warehouse'].sudo().search(domain, limit=1)
    warehouse_name = warehouse.name
    warehouse_code = warehouse.code

    terminal.update_tmp_values({
        'warehouse_id': warehouse_id,
        'warehouse_code': warehouse_code,
        'warehouse_name': warehouse_name,
    })

act = 'L'

warehouse_picking_type_ids = env['stock.picking.type'].sudo().search([
    ('warehouse_id', '=', warehouse_id)
])

res = [
    ('|', 'Picking type({0})'.format(terminal.get_tmp_value('warehouse_name', False))),

]

for picking_type_id in warehouse_picking_type_ids:
    res.append((picking_type_id.id, picking_type_id.name))
