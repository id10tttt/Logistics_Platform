'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

terminal.clean_tmp_values(['sku_code'])

move_id = message
# 保存move_line_id
if not terminal.get_tmp_value('move_id', False):
    terminal.update_tmp_values({'move_id': move_id})

move_id = env['stock.move'].sudo().browse(terminal.get_tmp_value('move_id'))

# 更新当前的 barcode
terminal.update_tmp_values({
    'sku_code': move_id.product_id.barcode,
})

print('move_id', move_id.read())
act = 'T'
res = [
    '|SKU({0})'.format(move_id.product_id.barcode),
]
