'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

print('tmp_values', terminal.tmp_values)

# 当前的 stock.picking(xxx,)
stock_picking_id = terminal.get_tmp_value('stock_picking_id', False)
if stock_picking_id:
    picking_id = env['stock.picking'].sudo().browse(stock_picking_id)
else:
    picking_id = env['stock.picking'].sudo().browse(message)

# 列出所有的 sku
move_lines = picking_id.move_lines

# 列出当前已经选择了的SKU code
current_sku_code = terminal.get_tmp_value('sku_code', False)

res = [
    ('|', 'Move({0})'.format(picking_id.name))
]

act = 'L'

if not terminal.get_tmp_value('stock_picking_id', False):
    terminal.update_tmp_values({'stock_picking_id': message})

for line_id in move_lines:
    if current_sku_code == line_id.product_id.barcode:
        res.append(
            (line_id.id, 'Done: ' + line_id.product_id.barcode)
        )
        if not terminal.get_tmp_value('done_move_ids', False):
            terminal.update_tmp_values({
                'done_sku_codes': [current_sku_code]
            })
        else:
            done_sku_codes = terminal.get_tmp_value('done_move_ids').append(current_sku_code)
            terminal.update_tmp_values({
                'done_sku_codes': done_sku_codes
            })
    else:
        res.append(
            (line_id.id, line_id.product_id.name + '/' + line_id.product_id.barcode)
        )

res.append(
    (0, 'Commit')
)
