'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

# 列出所有的 stock picking
picking_type_id = message

if not terminal.get_tmp_value('picking_type_id', False):
    terminal.update_tmp_values({'picking_type_id': picking_type_id})

# 使用cache 参数
picking_type_id = env['stock.picking.type'].sudo().browse(terminal.get_tmp_value('picking_type_id'))
picking_ids = env['stock.picking'].sudo().search([
    ('picking_type_id', '=', terminal.get_tmp_value('picking_type_id'))
])

res = [
    ('|', 'Picking({0})'.format(picking_type_id.name))
]

act = 'L'

for picking_id in picking_ids:
    res.append(
        (picking_id.id, picking_id.name)
    )
