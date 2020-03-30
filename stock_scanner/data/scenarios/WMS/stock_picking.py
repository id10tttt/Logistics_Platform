'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

if message == 0:
    # 提交
    stock_picking_id = terminal.get_tmp_value('stock_picking_id', False)
    sku_count = terminal.get_tmp_value('sku_count', False)
    # 获取 stock picking  和 数量
    if stock_picking_id and sku_count:
        stock_picking_id = env['stock.picking'].sudo().browse(stock_picking_id)
        # 完成部分，不创建欠单

        # step 1: 新增 stock.move.line
        # step 2: 没有欠单

        # step1
        move_lines = stock_picking_id.move_lines
        create_move_line = []
        for move_line in move_lines:
            sku_amount = sku_count.get(move_line.product_id.barcode)

            # 创建 move line
            tmp = {
                'picking_id': stock_picking_id.id,
                'move_id': move_line.id,
                'location_id': move_line.location_id.id,
                'location_dest_id': move_line.location_dest_id.id,
                'product_uom_qty': move_line.product_uom_qty,
                'qty_done': sku_amount,
                'product_id': move_line.product_id.id,
                'product_uom_id': move_line.product_id.uom_id.id,
            }
            create_move_line.append(tmp)
        # 创建
        res = env['stock.move.line'].sudo().create(create_move_line)
        no_back_order = env['stock.backorder.confirmation'].sudo().create({
            'pick_ids': [(6, 0, stock_picking_id.ids)]
        })
        no_back_order.sudo().process_cancel_backorder()

terminal.clean_tmp_values(['sku_code', 'current_sku_code', 'sku_count', 'stock_picking_id', 'move_id'])

# 列出所有的 stock picking
picking_type_id = message

if not terminal.get_tmp_value('picking_type_id', False):
    terminal.update_tmp_values({'picking_type_id': picking_type_id})

# 使用cache 参数
picking_type_id = env['stock.picking.type'].sudo().browse(terminal.get_tmp_value('picking_type_id'))

# 筛选出picking type， 状态为 就绪的 picking
picking_ids = env['stock.picking'].sudo().search([
    ('picking_type_id', '=', terminal.get_tmp_value('picking_type_id')),
    ('state', '=', 'assigned')
])

res = [
    ('|', 'Picking({0})'.format(picking_type_id.name))
]

act = 'L'

for picking_id in picking_ids:
    res.append(
        (picking_id.id, picking_id.name)
    )
