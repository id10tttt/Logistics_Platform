
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

# 清除步骤
terminal.clean_tmp_values(['picking_type_name'])

# 操作后清除临时数据,但保留仓库的信息
filter_clean_keys = [ 'warehouse_id', 
                      'warehouse_code', 
                      'warehouse_name', 
                      'lot_stock_id',
                      'lot_stock_name',
                      ]
all_keys = list(terminal.tmp_values.keys())
terminal.clean_tmp_values( list(set(all_keys).difference(set(filter_clean_keys)))  )

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
  lot_stock_id = warehouse.lot_stock_id.id
  lot_stock_name = warehouse.lot_stock_id.display_name
  
  
  #保存仓库id/code/名称
  terminal.update_tmp_values({
    'warehouse_id': warehouse_id,
    'warehouse_code': warehouse_code,
    'warehouse_name': warehouse_name,
    'lot_stock_id': lot_stock_id,
    'lot_stock_name': lot_stock_name,
    
  })
  
  
act = 'L'

picking_type = ['入库',
                '出库',
                '返回',
                
          ]


res = [
    ('|','步骤({0})'.format(terminal.get_tmp_value('warehouse_name', False))),
    
]

for item in picking_type:
    res.append((item, item))