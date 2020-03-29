'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

# 列出所有的 stock picking
picking_type_id = message

picking_type_id = env['stock.picking.type'].sudo().browse(picking_type_id)
picking_ids = env['stock.picking'].sudo().search([
    ('picking_type_id', '=', message)
])

res = [
    ('|', 'Picking({0})'.format(picking_type_id.name))
]

act = 'L'

for picking_id in picking_ids:
    res.append(
        (picking_id.id, picking_id.name)
    )
