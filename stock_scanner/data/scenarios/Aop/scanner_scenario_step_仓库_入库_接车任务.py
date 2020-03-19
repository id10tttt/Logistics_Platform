
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

# 可选择本仓库或者父仓库的接车任务
stock_picking = env['stock.picking'].sudo().search([
                        ('picking_type_id.name', 'in', ['接车', '短驳接车']),
                        ('state', 'in', ['draft', 'waiting', 'assigned']),
                        # ('batch_id', '!=', False),
                        ('picking_type_id.warehouse_id.name', 'in', [terminal.get_tmp_value('warehouse_name', False), terminal.get_tmp_value('parent_warehouse_name', False)]),
                        # ('picking_type_id.warehouse_id.name', 'in', ['团结村总库', '团结村快运库']),
                        
                    ])

  
act = 'L'

res = [
  ('|', '任务')
]

for item in stock_picking:
  res.append((item.id, '{0}/{1}/数量:{2}'.format(item.location_id.name, item.location_dest_id.name, item.picking_incoming_number )))
  
  
