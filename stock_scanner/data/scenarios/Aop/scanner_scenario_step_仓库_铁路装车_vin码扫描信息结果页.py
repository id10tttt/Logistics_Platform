
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

vin_code = message

# 查找任务
stock_picking = env['stock.picking'].sudo().search([
                        ('vin_id.name', '=', vin_code),
                        ('picking_type_id.name', '=', terminal.get_tmp_value('picking_type_name', False)),
                        ('picking_type_id.warehouse_id.name', '=', terminal.get_tmp_value('warehouse_name', False)),
                        ('state', '=', 'assigned')
                    ], limit=1)

if not stock_picking:
  act = 'E'
  res = [
      '',
      '',
      'VIN: {0}, 没有查到任务'.format(vin_code),
  ]
  val = True
  
else:

  params = terminal.get_tmp_value('params',  dict())
  
  # 货线
  train_manage_id = terminal.get_tmp_value('train_manage_id', False)
  
  # 车厢号
  train_manage_line_id = terminal.get_tmp_value('train_manage_line_id', False)
  train_manage_line_name = terminal.get_tmp_value('train_manage_line_name', False)
  
  # 上/下层
  layer_option = terminal.get_tmp_value('layer_option', False)
  layer_option_cn = terminal.get_tmp_value('layer_option_cn', False)
  
  
  # 任务id/name,产品名称,批次号
  stock_picking_id = stock_picking.id
  stock_picking_name = stock_picking.name
  batch_id = stock_picking.batch_id.id
  product_name = ''
  
  for line in stock_picking.move_ids_without_package:
    product_name = line.product_id.name
  
 
  params.update({vin_code: {'train_manage_id': train_manage_id,
                            'train_manage_line_id': train_manage_line_id,
                            'train_manage_line_name': train_manage_line_name,
                            'layer_option': layer_option,
                            'layer_option_cn': layer_option_cn,
                            'stock_picking_id': stock_picking_id,
                            'stock_picking_name': stock_picking_name,
                            'product_name': product_name,
                            'batch_id': batch_id,
                            
  }})
  terminal.update_tmp_values({'params': params})
  params_lst = list( terminal.get_tmp_value('params', False).keys() )

  count = len(params_lst)
  
  terminal.update_tmp_values({'vin_scan_count': count})
  
  # 如果装车、加固只扫一次，那么还需要找出加固任务
  scanner_step = terminal.get_tmp_value('scanner_step', 'once')
  if scanner_step == 'once':
    jiagu_params = terminal.get_tmp_value('jiagu_params', [])
    
    # 查找加固任务,这里写死步骤名称
    stock_picking = env['stock.picking'].sudo().search([
                            ('vin_id.name', '=', vin_code),
                            ('picking_type_id.name', '=', '加固'),
                            ('picking_type_id.warehouse_id.name', '=', terminal.get_tmp_value('warehouse_name', False)),
                            ('state', '=', 'waiting')
                        ], limit=1)
    
    if stock_picking:
      jiagu_params.append(stock_picking.id)
      terminal.update_tmp_values({'jiagu_params': jiagu_params})
      
  
  act = 'C'
  
  res = [
      ('|', '结果页'),
      '',
      '是否继续扫描VIN码?',
      '',
      '',
      
  ]
  
  res.append('VIN码: {0}'.format(vin_code))
  res.append('')
  res.append('合计已扫描VIN码数量: {0}'.format(count))  
