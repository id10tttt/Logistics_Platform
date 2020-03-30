'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

terminal.clean_tmp_values(['move_id'])

# 保存上级 picking id
if not terminal.get_tmp_value('stock_picking_id', False):
    terminal.update_tmp_values({'stock_picking_id': message})

print('message: ', message)
# 当前的 stock.picking(xxx,)

stock_picking_id = terminal.get_tmp_value('stock_picking_id', False)
if stock_picking_id:
    picking_id = env['stock.picking'].sudo().browse(stock_picking_id)
else:
    picking_id = env['stock.picking'].sudo().browse(message)

# 列出所有的 sku
move_lines = picking_id.move_lines

# 列出当前已经选择了的SKU code
# 需要记录已经扫描过的SKU的次数
# 当前 SKU
current_sku_code = terminal.get_tmp_value('sku_code', False)

# 新增 sku_count key
# 空字典
if not terminal.get_tmp_value('sku_count', False):
    terminal.update_tmp_values({
        'sku_count': {

        }
    })

# 保存记录
if current_sku_code:
    # 如果还没有这条记录，需要先保存，如果已经存在，+1
    sku_count = terminal.get_tmp_value('sku_count')

    if current_sku_code in sku_count.keys():
        sku_count.update({
            current_sku_code: sku_count.get(current_sku_code) + 1
        })
        terminal.update_tmp_values({
            'sku_count': sku_count
        })
    else:
        sku_count.update({
            current_sku_code: 1
        })
        terminal.update_tmp_values({
            'sku_count': sku_count
        })

# Title
res = [
    ('|', 'Move({0})'.format(picking_id.name))
]

# action type <list>
act = 'L'

for line_id in move_lines:
    # 在 sku_count 里面查找，是否包含当前的 sku
    sku_count = terminal.get_tmp_value('sku_count', {})
    if line_id.product_id.barcode in sku_count.keys():
        res.append(
            (line_id.id, 'Done: [{}/{}], '.format(sku_count.get(line_id.product_id.barcode),
                                                  int(line_id.product_uom_qty)) + line_id.product_id.barcode)
        )
    else:
        res.append(
            (line_id.id, line_id.product_id.name + '/' + line_id.product_id.barcode)
        )

res.append(
    (0, 'Commit')
)
